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

import datamaxi._ws_models as _ws_models  # noqa: E402
from datamaxi.aio.ws import AsyncDatamaxiWS, build_param  # noqa: E402
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


def test_ws_orderbook_excluded():
    assert not any("orderbook" in p for p in WS_CHANNELS)


def test_ws_every_channel_has_a_generated_model_and_accessor():
    # Every generated channel maps to a real model in _ws_models...
    for path, ch in WS_CHANNELS.items():
        assert hasattr(_ws_models, ch["message"]), f"{path}: missing {ch['message']}"
    # ...and the client exposes an accessor for every data type.
    ws = AsyncDatamaxiWS(api_key="k")
    for name in (
        "ticker",
        "forex",
        "premium",
        "funding_rate",
        "open_interest",
        "liquidation",
        "liquidation_feed",
        "announcement",
        "announcement_internal",
    ):
        assert hasattr(ws, name), f"client missing ws.{name}"


def test_ws_param_format_from_registry():
    ws = AsyncDatamaxiWS(api_key="k")
    assert ws.premium.param_format == "src:tgt:tokenId:srcQuote:tgtQuote:srcMkt:tgtMkt"
    assert ws.forex.param_format == "SYMBOL"


def test_ws_forex_subscribe_streams():
    async def handler(conn):
        seen = None
        async for raw in conn:
            m = json.loads(raw)
            if m.get("method") == "SUBSCRIBE":
                seen = (conn.request.path, m["params"])
                await conn.send(json.dumps({"result": m["params"], "id": m["id"]}))
                await conn.send(json.dumps({"s": "USD-KRW", "d": 1, "r": 1530.0}))
                assert seen == ("/ws/v1/forex", ["USD-KRW"])

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k", ws_url=f"ws://localhost:{_port(server)}"
            ) as ws:
                stream = await ws.forex.subscribe("USD-KRW")
                return await _first(stream)

    assert _run(run()) == {"s": "USD-KRW", "d": 1, "r": 1530.0}


def test_ws_liquidation_feed_streams_without_subscribe():
    async def handler(conn):
        # firehose: push immediately, no SUBSCRIBE expected
        await conn.send(json.dumps({"s": "RPL-USDT", "sd": "sell", "p": 2.2}))
        async for _ in conn:
            pass

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k", ws_url=f"ws://localhost:{_port(server)}"
            ) as ws:
                stream = await ws.liquidation_feed.stream()
                return await _first(stream)

    assert _run(run())["s"] == "RPL-USDT"


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


def test_ws_empty_result_ack_is_filtered():
    # When the accepted param list is empty the server omits `result`, sending
    # just {"id": N}. That must be filtered, not yielded as data. (A data
    # payload can itself carry an "id" token, e.g. {"id": "bitcoin", ...}.)
    async def handler(conn):
        async for raw in conn:
            m = json.loads(raw)
            if m.get("method") == "SUBSCRIBE":
                await conn.send(json.dumps({"id": m["id"]}))  # empty-result ack
                await conn.send(
                    json.dumps({"id": "bitcoin", "s": "BTC-USDT", "p": 1.0})
                )

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k", ws_url=f"ws://localhost:{_port(server)}"
            ) as ws:
                stream = await ws.ticker.subscribe("BTC-USDT@binance", market="spot")
                return await _first(stream)

    msg = _run(run())
    assert msg == {"id": "bitcoin", "s": "BTC-USDT", "p": 1.0}  # data, not the ack


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


def test_ws_reconnect_replays_active_subscription(monkeypatch):
    # Drop the connection mid-stream and assert the client reconnects and
    # replays its active SUBSCRIBE, then resumes streaming. `_RECONNECT_BACKOFF`
    # is a module global read at call time in `_reader`, so shrink it to keep
    # the test fast.
    monkeypatch.setattr("datamaxi.aio.ws._RECONNECT_BACKOFF", 0.01)

    seen = []  # SUBSCRIBE params observed, one entry per connection

    async def handler(conn):
        idx = len(seen)
        seen.append(None)
        async for raw in conn:
            m = json.loads(raw)
            if m.get("method") == "SUBSCRIBE":
                seen[idx] = m["params"]
                await conn.send(json.dumps({"result": m["params"], "id": m["id"]}))
                if idx == 0:
                    # first connection: stream one message then drop it
                    await conn.send(json.dumps({"s": "USD-KRW", "d": 1, "r": 1.0}))
                    return  # returning closes the conn -> client reconnects
                # reconnect: send a distinguishable message, keep the conn open
                await conn.send(json.dumps({"s": "USD-KRW", "d": 2, "r": 2.0}))

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k",
                ws_url=f"ws://localhost:{_port(server)}",
                keepalive=0,  # no PING noise
            ) as ws:
                stream = await ws.forex.subscribe("USD-KRW")
                first = await _first(stream)
                # reading the second message forces the reconnect path to
                # complete (resubscribe + resume)
                second = await _first(stream)
                return first, second

    first, second = _run(run())
    assert first == {"s": "USD-KRW", "d": 1, "r": 1.0}
    assert second == {"s": "USD-KRW", "d": 2, "r": 2.0}  # post-reconnect payload
    # the server saw two connections and the reconnect replayed the active params
    assert len(seen) >= 2
    assert seen[0] == ["USD-KRW"]
    assert seen[1] == ["USD-KRW"]  # `_open` replays sorted(self._active)


# --- structured subscribe helpers: build_param unit tests ---


def test_build_param_forex_single_token():
    # SYMBOL: no separator, one token; and the SYMBOL->symbol lowercase rule.
    assert build_param("SYMBOL", symbol="USD-KRW") == "USD-KRW"


def test_build_param_symbol_exchange():
    assert (
        build_param("SYMBOL@exchange", symbol="BTC-USDT", exchange="binance")
        == "BTC-USDT@binance"
    )


def test_build_param_ticker_without_optional_group():
    fmt = "SYMBOL@exchange[@currency@conversionBase]"
    assert build_param(fmt, symbol="BTC-USDT", exchange="binance") == "BTC-USDT@binance"


def test_build_param_ticker_with_optional_group():
    fmt = "SYMBOL@exchange[@currency@conversionBase]"
    assert (
        build_param(
            fmt,
            symbol="BTC-USDT",
            exchange="binance",
            currency="KRW",
            conversionBase="USDT",
        )
        == "BTC-USDT@binance@KRW@USDT"
    )


def test_build_param_premium_all_seven_tokens():
    fmt = "src:tgt:tokenId:srcQuote:tgtQuote:srcMkt:tgtMkt"
    assert (
        build_param(
            fmt,
            src="binance",
            tgt="upbit",
            tokenId="bitcoin",
            srcQuote="USDT",
            tgtQuote="KRW",
            srcMkt="spot",
            tgtMkt="spot",
        )
        == "binance:upbit:bitcoin:USDT:KRW:spot:spot"
    )


def test_build_param_verbatim_token_not_lowercased():
    # tokenId is mixed-case, so it stays verbatim (not lowercased).
    with pytest.raises(ValueError):
        build_param(
            "src:tgt:tokenId:srcQuote:tgtQuote:srcMkt:tgtMkt",
            src="a",
            tgt="b",
            tokenid="c",  # wrong: lowercased key
            srcQuote="d",
            tgtQuote="e",
            srcMkt="f",
            tgtMkt="g",
        )


def test_build_param_none_channel_rejects_tokens():
    with pytest.raises(ValueError):
        build_param(None, symbol="X")


def test_build_param_missing_required_token():
    with pytest.raises(ValueError) as ei:
        build_param("SYMBOL@exchange", symbol="BTC-USDT")
    assert "exchange" in str(ei.value)


def test_build_param_unknown_token():
    with pytest.raises(ValueError) as ei:
        build_param("SYMBOL@exchange", symbol="BTC-USDT", exchange="binance", bogus="x")
    assert "bogus" in str(ei.value)


def test_build_param_partial_optional_group_rejected():
    fmt = "SYMBOL@exchange[@currency@conversionBase]"
    with pytest.raises(ValueError):
        build_param(fmt, symbol="BTC-USDT", exchange="binance", currency="KRW")


def test_build_param_roundtrip_matches_raw_ticker():
    fmt = WS_CHANNELS["/ticker/spot"]["param"]
    assert build_param(fmt, symbol="BTC-USDT", exchange="binance") == "BTC-USDT@binance"


def test_build_param_roundtrip_matches_raw_premium():
    fmt = WS_CHANNELS["/premium"]["param"]
    assert (
        build_param(
            fmt,
            src="binance",
            tgt="upbit",
            tokenId="bitcoin",
            srcQuote="USDT",
            tgtQuote="KRW",
            srcMkt="spot",
            tgtMkt="spot",
        )
        == "binance:upbit:bitcoin:USDT:KRW:spot:spot"
    )


def test_ws_structured_subscribe_produces_expected_wire_param():
    # A structured subscribe(...) call sends the same wire param as the raw form.
    async def handler(conn):
        async for raw in conn:
            m = json.loads(raw)
            if m.get("method") == "SUBSCRIBE":
                await conn.send(json.dumps({"result": m["params"], "id": m["id"]}))
                for p in m["params"]:
                    sym, exch = p.split("@")[0], p.split("@")[1]
                    await conn.send(
                        json.dumps({"s": sym, "e": exch, "p": 1.0, "d": 1, "_param": p})
                    )

    async def run():
        async with _serve(handler) as server:
            async with AsyncDatamaxiWS(
                api_key="k", ws_url=f"ws://localhost:{_port(server)}"
            ) as ws:
                stream = await ws.ticker.subscribe(
                    symbol="BTC-USDT", exchange="binance", market="spot"
                )
                return await _first(stream)

    msg = _run(run())
    assert msg["_param"] == "BTC-USDT@binance"


def test_ws_structured_subscribe_mixing_raw_and_tokens_raises():
    async def run():
        async with AsyncDatamaxiWS(api_key="k", ws_url="ws://localhost:1") as ws:
            await ws.forex.subscribe("USD-KRW", symbol="USD-KRW")

    with pytest.raises(ValueError):
        _run(run())
