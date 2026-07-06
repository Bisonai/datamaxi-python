"""Keyed live/integration lane for sporadic WS channels.

The offline `test_ws.py` covers the protocol against a local server. These
tests hit the real DataMaxi+ WS API for the two event-driven channels that
only got ack-level live checks — `/liquidation` (subscribe-only) and
`/announcement/listing` (Pro+). Both are sporadic, so a quiet window (no event
in the timeout) is a PASS: the value is that connect + auth + SUBSCRIBE succeed
without raising. Opt-in and deselected from the keyless CI lane via the
`integration` marker; needs DATAMAXI_API_KEY. Skipped when `websockets` absent.
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
