"""Local tests for the async WebSocket ticker client (pilot).

Runs a real in-process `websockets` server implementing the subscribe protocol,
so the client is exercised end-to-end (auth header, path, SUBSCRIBE, streamed
data, ack filtering, keepalive PING). Skipped when the optional `websockets`
dependency is absent.
"""

import asyncio
import json

import pytest

websockets = pytest.importorskip("websockets")

from datamaxi.aio.ws import AsyncDatamaxiWS  # noqa: E402
from datamaxi._ws_endpoints import WS_CHANNELS, WS_BASE_PATH  # noqa: E402
from datamaxi._ws_models import TickerMessage  # noqa: E402


def _serve(handler):
    return websockets.serve(handler, "localhost", 0)


def _port(server):
    return server.sockets[0].getsockname()[1]


async def _first(stream, timeout=2.0):
    return await asyncio.wait_for(stream.__anext__(), timeout)


def _run(coro):
    return asyncio.run(coro)


def test_ws_consumes_generated_registry_and_model():
    # The client resolves the path from the generated WS_CHANNELS, and the
    # generated TickerMessage carries the wire keys.
    assert "/ticker/spot" in WS_CHANNELS
    assert WS_CHANNELS["/ticker/spot"]["message"] == "TickerMessage"
    assert WS_BASE_PATH == "/ws/v1"
    assert {"p", "e", "s", "d"} <= set(TickerMessage.__annotations__)


def test_ws_ticker_subscribe_streams_and_filters_ack():
    seen = {}

    async def handler(conn):
        seen["apikey"] = conn.request.headers.get("X-DTMX-APIKEY")
        seen["path"] = conn.request.path
        async for raw in conn:
            m = json.loads(raw)
            if m.get("method") == "SUBSCRIBE":
                seen["params"] = m["params"]
                await conn.send(json.dumps({"result": m["params"], "id": m["id"]}))
                for p in m["params"]:
                    sym, exch = p.split("@")[0], p.split("@")[1]
                    await conn.send(
                        json.dumps({"s": sym, "e": exch, "p": 105.5, "d": 1})
                    )

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k", ws_url=f"ws://localhost:{_port(server)}"
            ) as ws:
                stream = await ws.ticker.subscribe("BTC-USDT@binance", market="spot")
                return await _first(stream)

    msg = _run(run())
    assert seen["apikey"] == "k"  # X-DTMX-APIKEY on the handshake
    assert seen["path"] == "/ws/v1/ticker/spot"  # base path + channel path
    assert seen["params"] == ["BTC-USDT@binance"]  # SUBSCRIBE protocol
    # first yielded item is data, not the {"result":...,"id":...} ack
    assert msg == {"s": "BTC-USDT", "e": "binance", "p": 105.5, "d": 1}


def test_ws_multi_symbol_multiplexed_on_one_connection():
    async def handler(conn):
        async for raw in conn:
            m = json.loads(raw)
            if m.get("method") == "SUBSCRIBE":
                await conn.send(json.dumps({"result": m["params"], "id": m["id"]}))
                for p in m["params"]:
                    sym = p.split("@")[0]
                    await conn.send(
                        json.dumps({"s": sym, "e": "binance", "p": 1.0, "d": 1})
                    )

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k", ws_url=f"ws://localhost:{_port(server)}"
            ) as ws:
                stream = await ws.ticker.subscribe(
                    "BTC-USDT@binance", "ETH-USDT@binance", market="spot"
                )
                got = {(await _first(stream))["s"], (await _first(stream))["s"]}
                return got

    assert _run(run()) == {"BTC-USDT", "ETH-USDT"}


def test_ws_keepalive_sends_ping():
    got_ping = asyncio.Event()

    async def handler(conn):
        async for raw in conn:
            if json.loads(raw).get("method") == "PING":
                got_ping.set()

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k",
                ws_url=f"ws://localhost:{_port(server)}",
                keepalive=0.1,
            ) as ws:
                await ws.ticker.subscribe("BTC-USDT@binance", market="spot")
                await asyncio.wait_for(got_ping.wait(), timeout=2.0)
                return True

    assert _run(run()) is True


def test_ws_invalid_market_raises():
    async def run():
        async with AsyncDatamaxiWS(api_key="k", ws_url="ws://localhost:1") as ws:
            await ws.ticker.subscribe("BTC-USDT@binance", market="bogus")

    with pytest.raises(ValueError):
        _run(run())


def test_ws_repr_no_key_leak():
    ws = AsyncDatamaxiWS(api_key="secret", base_url="https://api.datamaxiplus.com")
    assert ws.ws_url == "wss://api.datamaxiplus.com"
    assert "secret" not in repr(ws)
    assert "has_key=True" in repr(ws)
