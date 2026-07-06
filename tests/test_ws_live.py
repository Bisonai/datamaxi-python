"""Keyed live/integration lane for the real DataMaxi+ WS API.

The offline `test_ws.py` covers the protocol against a local server. These
tests hit prod. Two kinds of channel:

- Sporadic (event-driven): `/liquidation`, `/announcement/listing`,
  `/funding-rate`, `/open-interest`, and `/forex` (weekends/off-hours). A quiet
  window (no message in the timeout) is a PASS — the value is that connect +
  auth + SUBSCRIBE succeed without raising; when a message does arrive its shape
  is still checked.
- High-traffic (continuous): `/ticker` and `/premium`. These emit non-stop, so
  a quiet window is a FAIL — the test asserts a real, well-formed data payload
  actually arrives, proving the SDK decodes and yields end-to-end.

Opt-in and deselected from the keyless CI lane via the `integration` marker;
needs DATAMAXI_API_KEY. Skipped when `websockets` absent.
"""

import asyncio

import pytest

websockets = pytest.importorskip("websockets")

from datamaxi.aio.ws import AsyncDatamaxiWS  # noqa: E402
from tests.conftest import API_KEY, BASE_URL  # noqa: E402

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not API_KEY,
        reason="API key not provided. Set DATAMAXI_API_KEY environment variable.",
    ),
]

# Sporadic channels may be silent for long stretches; a quiet window is a pass.
_QUIET_TIMEOUT = 10.0
# High-traffic channels emit continuously, so a quiet window is a FAIL. ticker
# ticks roughly every ~10s in practice; give headroom so one slow tick can't flake.
_DATA_TIMEOUT = 30.0
# /forex is quiet-tolerant but its first tick can lag (~14s observed); wait a bit
# longer than _QUIET_TIMEOUT so an arriving tick gets shape-checked, not skipped.
_FOREX_TIMEOUT = 20.0


def _run(coro):
    return asyncio.run(coro)


def test_ws_liquidation_subscribe_tolerates_quiet_window():
    # /liquidation is subscribe-only and event-driven (basic tier). Param format
    # is "SYMBOL@exchange" per the generated registry.
    async def run():
        async with AsyncDatamaxiWS(api_key=API_KEY, base_url=BASE_URL) as ws:
            stream = await ws.liquidation.subscribe("BTC-USDT@binance")
            try:
                return await asyncio.wait_for(stream.__anext__(), _QUIET_TIMEOUT)
            except asyncio.TimeoutError:
                # quiet window: connect + auth + SUBSCRIBE ok, just no event
                return None

    msg = _run(run())
    if msg is not None:
        assert isinstance(msg, dict)


def test_ws_announcement_subscribe_tolerates_quiet_window():
    # /announcement/listing is Pro+ and takes no param. A non-Pro key is
    # rejected either at the handshake (InvalidStatus, a WebSocketException) or
    # by a close right after connect. reconnect=False makes that post-connect
    # close deterministic: the reader stops instead of reconnect-looping, so the
    # stream ends and __anext__ raises StopAsyncIteration. Skip on either so a
    # Basic key doesn't red the lane; a Pro key streams (or hits the quiet-window
    # timeout) for real. A quiet Pro connection stays open -> TimeoutError -> pass.
    async def run():
        async with AsyncDatamaxiWS(
            api_key=API_KEY, base_url=BASE_URL, reconnect=False
        ) as ws:
            stream = await ws.announcement.subscribe()
            try:
                return await asyncio.wait_for(stream.__anext__(), _QUIET_TIMEOUT)
            except asyncio.TimeoutError:
                # quiet window: subscribed fine, just no listing event
                return None

    try:
        msg = _run(run())
    except (websockets.exceptions.WebSocketException, StopAsyncIteration) as exc:
        pytest.skip(f"/announcement/listing rejected (needs Pro+ tier): {exc!r}")
    if msg is not None:
        assert isinstance(msg, dict)


def test_ws_ticker_yields_live_data():
    # /ticker (spot) is high-traffic: it emits continuously, so a quiet window is
    # a FAIL, not a pass. Unlike the sporadic channels above, this proves the SDK
    # decodes and yields a real payload end-to-end — connect + auth + SUBSCRIBE +
    # an actual well-formed data message for BTC-USDT@binance within the timeout.
    async def run():
        async with AsyncDatamaxiWS(api_key=API_KEY, base_url=BASE_URL) as ws:
            stream = await ws.ticker.subscribe("BTC-USDT@binance", market="spot")
            return await asyncio.wait_for(stream.__anext__(), _DATA_TIMEOUT)

    msg = _run(run())
    assert isinstance(msg, dict)
    assert msg["s"] == "BTC-USDT"
    assert "p" in msg


def test_ws_premium_yields_live_data():
    # /premium (cross-exchange premium) is high-traffic: crypto premium trades
    # 24/7, so — like ticker — a quiet window is a FAIL. Proves the SDK decodes
    # and yields a real premium payload end-to-end. The `premium` value itself
    # can be null, so assert on stable identity fields, not the value.
    key = "binance:upbit:bitcoin:USDT:KRW:spot:spot"

    async def run():
        async with AsyncDatamaxiWS(api_key=API_KEY, base_url=BASE_URL) as ws:
            stream = await ws.premium.subscribe(key)
            return await asyncio.wait_for(stream.__anext__(), _DATA_TIMEOUT)

    msg = _run(run())
    assert isinstance(msg, dict)
    assert msg["key"] == key
    assert "premium" in msg


def test_ws_forex_tolerates_quiet_window():
    # /forex is continuous during FX market hours but the first tick can lag
    # (~14s observed) and FX spot does not trade weekends — so a quiet window is
    # a legitimate PASS (like the sporadic channels). When a tick does arrive,
    # validate its shape.
    async def run():
        async with AsyncDatamaxiWS(api_key=API_KEY, base_url=BASE_URL) as ws:
            stream = await ws.forex.subscribe("USD-KRW")
            try:
                return await asyncio.wait_for(stream.__anext__(), _FOREX_TIMEOUT)
            except asyncio.TimeoutError:
                # quiet window (off-hours/weekend): subscribed fine, just no tick
                return None

    msg = _run(run())
    if msg is not None:
        assert isinstance(msg, dict)
        assert msg["s"] == "USD-KRW"
        assert "r" in msg


def test_ws_funding_rate_tolerates_quiet_window():
    # /funding-rate pushes on-change/snapshot — sporadic (0 msgs in a 20s probe),
    # so a quiet window is a PASS. Shape wasn't observable live; when a message
    # does arrive, assert only that it's a non-empty data dict (acks are already
    # filtered by the client's reader).
    async def run():
        async with AsyncDatamaxiWS(api_key=API_KEY, base_url=BASE_URL) as ws:
            stream = await ws.funding_rate.subscribe("BTC-USDT@binance")
            try:
                return await asyncio.wait_for(stream.__anext__(), _QUIET_TIMEOUT)
            except asyncio.TimeoutError:
                return None

    msg = _run(run())
    if msg is not None:
        assert isinstance(msg, dict)
        assert msg


def test_ws_open_interest_tolerates_quiet_window():
    # /open-interest is sporadic (0 msgs in a 20s probe), so a quiet window is a
    # PASS. Shape wasn't observable live; when a message does arrive, assert only
    # that it's a non-empty data dict (acks are already filtered by the reader).
    async def run():
        async with AsyncDatamaxiWS(api_key=API_KEY, base_url=BASE_URL) as ws:
            stream = await ws.open_interest.subscribe("BTC-USDT@binance")
            try:
                return await asyncio.wait_for(stream.__anext__(), _QUIET_TIMEOUT)
            except asyncio.TimeoutError:
                return None

    msg = _run(run())
    if msg is not None:
        assert isinstance(msg, dict)
        assert msg
