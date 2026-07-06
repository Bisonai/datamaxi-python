"""Async coverage for the full resource tree (#142 expansion).

Routes requests by path through one httpx.MockTransport and checks each
resource's ported method returns/awaits correctly, including the async
`next_request` pagination closures. Skipped when httpx is absent.
"""

import asyncio

import pytest

httpx = pytest.importorskip("httpx")

from datamaxi.aio import AsyncDatamaxi  # noqa: E402
from datamaxi.aio.telegram import AsyncTelegram  # noqa: E402
from datamaxi.aio.naver import AsyncNaver  # noqa: E402

BASE_URL = "https://api.datamaxiplus.com"

_FEE = [{"exchange": "binance", "symbol": "BTC-USDT", "maker": "0.001"}]
_STATUS = [{"network": "BSC", "currency": "USDT"}]
_ANNOUNCE = {"data": [{"t": "New listing", "e": "binance"}]}
_UPDATES = {"data": [{"b": "BTC", "t": "listed"}]}
_META = {"BTC": {"status": "trading"}}
_HISTORY = {"data": [{"d": "1700000000", "f": "0.0001"}]}
_LATEST = {"d": "1700000000", "f": "0.0001", "s": "BTC-USDT"}
_FOREX = {"d": "1700000000", "r": "1380.5", "s": "USD-KRW"}
_PREMIUM = {
    "data": [
        {
            "detail": {"bid": "BTC"},
            "source_annualized_funding_rate": "0",
            "target_annualized_funding_rate": "0",
        }
    ]
}
_HEATMAP = {"data": {"binance": {"BTC": "1"}}}
_OI = {"data": {"oi": "1"}}
_MARGIN = {"data": {"rate": "1"}}
_INDEX = {"data": [{"d": "1", "p": "1"}]}
_CHANNELS = {"data": [{"channelName": "alpha", "category": "news"}]}
_MESSAGES = {"data": [{"channelName": "alpha", "message": "gm"}]}
_TREND = [{"d": "2024-01-01", "v": 10}]

ROUTES = {
    "/api/v1/cex/fees": _FEE,
    "/api/v1/wallet-status": _STATUS,
    "/api/v1/cex/announcements": _ANNOUNCE,
    "/api/v1/cex/token/updates": _UPDATES,
    "/api/v1/cex/symbol/metadata": _META,
    "/api/v1/funding-rate/history": _HISTORY,
    "/api/v1/funding-rate/latest": _LATEST,
    "/api/v1/forex": _FOREX,
    "/api/v1/premium": _PREMIUM,
    "/api/v1/liquidation/heatmap": _HEATMAP,
    "/api/v1/open-interest": _OI,
    "/api/v1/margin-borrow": _MARGIN,
    "/api/v1/index-price": _INDEX,
    "/api/v1/telegram/channels": _CHANNELS,
    "/api/v1/telegram/messages": _MESSAGES,
    "/api/v1/naver-trend": _TREND,
}


def _handler(request):
    payload = ROUTES.get(request.url.path)
    if payload is None:  # unexpected path -> fail loudly
        return httpx.Response(404, json={"error": "no route for " + request.url.path})
    return httpx.Response(200, json=payload)


def _transport():
    return httpx.MockTransport(_handler)


def _dm():
    return AsyncDatamaxi(api_key="k", base_url=BASE_URL, transport=_transport())


def _run(coro):
    return asyncio.run(coro)


def test_async_cex_fee():
    async def run():
        async with _dm() as c:
            return await c.cex.fee(exchange="binance")

    assert _run(run()) == _FEE


def test_async_cex_wallet_status_pandas_false():
    async def run():
        async with _dm() as c:
            return await c.cex.wallet_status(
                exchange="binance", asset="USDT", pandas=False
            )

    assert _run(run()) == _STATUS


def test_async_cex_symbol_metadata():
    async def run():
        async with _dm() as c:
            return await c.cex.symbol.metadata(base="BTC")

    assert _run(run()) == _META


def test_async_forex_single_object():
    async def run():
        async with _dm() as c:
            return await c.forex(symbol="USD-KRW", pandas=False)

    assert _run(run()) == _FOREX


def test_async_premium_envelope():
    async def run():
        async with _dm() as c:
            return await c.premium(pandas=False)

    assert _run(run()) == _PREMIUM


def test_async_futures_surfaces_raw():
    async def run():
        async with _dm() as c:
            return (
                await c.liquidation.heatmap(),
                await c.open_interest(exchange="binance", symbol="BTC-USDT"),
                await c.margin_borrow(asset="BTC"),
                await c.index_price(asset="BTC"),
            )

    hm, oi, mb, ip = _run(run())
    assert (hm, oi, mb, ip) == (_HEATMAP, _OI, _MARGIN, _INDEX)


def test_async_naver_trend_and_symbols():
    async def run():
        async with AsyncNaver(
            api_key="k", base_url=BASE_URL, transport=_transport()
        ) as n:
            return await n.trend("BTC", pandas=False)

    assert _run(run()) == _TREND


def test_async_pagination_next_request_is_awaitable():
    # announcement / token / funding.history / telegram all return
    # (envelope, async next_request); the closure must be awaitable.
    async def run():
        async with _dm() as c:
            res, nxt = await c.cex.announcement()
            assert res == _ANNOUNCE
            assert asyncio.iscoroutinefunction(nxt)
            res2, nxt2 = await nxt()  # awaiting the next page works
            return res2

    assert _run(run()) == _ANNOUNCE


def test_async_telegram_pagination():
    async def run():
        async with AsyncTelegram(
            api_key="k", base_url=BASE_URL, transport=_transport()
        ) as t:
            res, nxt = await t.channels()
            assert asyncio.iscoroutinefunction(nxt)
            return res

    assert _run(run()) == _CHANNELS


def test_standalone_async_clients_not_top_level_importable():
    import datamaxi.aio

    assert not hasattr(datamaxi.aio, "AsyncTelegram")
    assert not hasattr(datamaxi.aio, "AsyncNaver")


def test_async_telegram_naver_mounted_reuse_shared_session():
    c = _dm()
    assert isinstance(c.telegram, AsyncTelegram)
    assert isinstance(c.naver, AsyncNaver)
    # Same shared AsyncAPI/transport as every other sub-resource.
    assert c.telegram._api is c._api
    assert c.naver._api is c._api
    assert c.telegram._api is c.cex._api


def test_async_mounted_telegram_and_naver_work():
    async def run():
        async with _dm() as c:
            channels, _ = await c.telegram.channels()
            messages, _ = await c.telegram.messages(channel_name="alpha")
            trend = await c.naver.trend("BTC", pandas=False)
            return channels, messages, trend

    channels, messages, trend = _run(run())
    assert channels == _CHANNELS
    assert messages == _MESSAGES
    assert trend == _TREND


def test_async_funding_history_and_latest():
    async def run():
        async with _dm() as c:
            hist, nxt = await c.funding_rate.history(
                exchange="binance", symbol="BTC-USDT", pandas=False
            )
            latest = await c.funding_rate.latest(
                exchange="binance", symbol="BTC-USDT", pandas=False
            )
            return hist, latest

    hist, latest = _run(run())
    assert hist == _HISTORY
    assert latest == _LATEST
