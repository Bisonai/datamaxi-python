"""Local tests for the async client pilot (#142).

Uses httpx.MockTransport (no network, no extra deps) injected into AsyncAPI.
Skipped entirely when the optional ``httpx`` dependency is absent.
"""

import asyncio

import pandas as pd
import pytest

httpx = pytest.importorskip("httpx")

from datamaxi.aio import AsyncDatamaxi  # noqa: E402
from datamaxi.api import ResponseMeta  # noqa: E402
from datamaxi.error import ClientError  # noqa: E402

BASE_URL = "https://api.datamaxiplus.com"
_CANDLE = {
    "data": [{"d": "1700000000", "o": "1", "h": "2", "l": "1", "c": "2", "v": "9"}]
}
_TICKER = {"data": {"d": "1700000000", "p": "105.5"}}


def _run(coro):
    return asyncio.run(coro)


def _client(handler):
    return AsyncDatamaxi(
        api_key="k", base_url=BASE_URL, transport=httpx.MockTransport(handler)
    )


def test_async_candle_returns_dataframe():
    def handler(request):
        assert request.url.path == "/api/v1/cex/candle"
        return httpx.Response(200, json=_CANDLE)

    async def run():
        async with _client(handler) as c:
            return await c.cex.candle(
                exchange="binance", market="spot", symbol="BTC-USDT"
            )

    df = _run(run())
    assert isinstance(df, pd.DataFrame)
    assert "c" in df.columns


def test_async_candle_pandas_false_returns_envelope():
    async def run():
        async with _client(lambda r: httpx.Response(200, json=_CANDLE)) as c:
            return await c.cex.candle(
                exchange="binance", market="spot", symbol="BTC-USDT", pandas=False
            )

    res = _run(run())
    assert res == _CANDLE


def test_async_ticker_forwards_bool_param_like_sync():
    seen = {}

    def handler(request):
        seen.update(dict(request.url.params))
        return httpx.Response(200, json=_TICKER)

    async def run():
        async with _client(handler) as c:
            return await c.cex.ticker.get(
                exchange="binance",
                market="spot",
                symbol="BTC-USDT",
                include_source=True,
            )

    df = _run(run())
    assert isinstance(df, pd.DataFrame)
    # bool encoded as "True" (matches the sync urlencode output), not "true"
    assert seen["include_source"] == "True"


def test_async_last_response_populated():
    headers = {"x-ratelimit-remaining": "42"}

    async def run():
        async with _client(
            lambda r: httpx.Response(200, json=_TICKER, headers=headers)
        ) as c:
            await c.cex.ticker.get(exchange="binance", market="spot", symbol="BTC-USDT")
            return c.cex.ticker.last_response

    lr = _run(run())
    assert isinstance(lr, ResponseMeta)
    assert lr.status_code == 200
    assert lr.limit_usage == {"x-ratelimit-remaining": "42"}


def test_async_client_error_raises():
    async def run():
        async with _client(
            lambda r: httpx.Response(400, json={"error": "bad request"})
        ) as c:
            await c.cex.ticker.get(exchange="binance", market="spot", symbol="BTC-USDT")

    with pytest.raises(ClientError):
        _run(run())


def test_async_retries_transient_5xx():
    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 3:
            return httpx.Response(503, json={"error": "busy"})
        return httpx.Response(200, json=_TICKER)

    async def run():
        async with AsyncDatamaxi(
            api_key="k",
            base_url=BASE_URL,
            retry_backoff=0.0,
            transport=httpx.MockTransport(handler),
        ) as c:
            return await c.cex.ticker.get(
                exchange="binance", market="spot", symbol="BTC-USDT"
            )

    df = _run(run())
    assert isinstance(df, pd.DataFrame)
    assert calls["n"] == 3  # 503, 503, 200


def test_async_invalid_market_raises_before_request():
    async def run():
        async with _client(lambda r: httpx.Response(200, json=_TICKER)) as c:
            await c.cex.candle(exchange="binance", market="bogus", symbol="BTC-USDT")

    with pytest.raises(ValueError):
        _run(run())
