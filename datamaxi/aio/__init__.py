"""Async client — ``httpx``-based mirror of the sync DataMaxi+ client.

Requires the ``async`` extra::

    pip install "datamaxi[async]"

Usage::

    from datamaxi.aio import AsyncDatamaxi

    async with AsyncDatamaxi(api_key="...") as client:
        df = await client.cex.candle(exchange="binance", market="spot",
                                     symbol="BTC-USDT")
        ticker = await client.cex.ticker.get(exchange="binance", market="spot",
                                             symbol="BTC-USDT")

Mirrors the full sync surface (``cex.*``, ``funding_rate``, ``forex``,
``premium``, ``liquidation``, ``open_interest``, ``margin_borrow``,
``index_price``, ``telegram``, ``naver``). The standalone
``AsyncTelegram`` / ``AsyncNaver`` classes stay exported for back-compat.
Reuses
the sync client's endpoint resolution and error handling (``datamaxi._dispatch``)
and the shared DataFrame / ResponseMeta helpers, so the two clients can't drift
on request building or error semantics.
"""

from typing import Any

from datamaxi.lib.constants import BASE_URL
from datamaxi.aio._core import AsyncAPI, AsyncResource
from datamaxi.aio.cex import (
    AsyncCex,
    AsyncCexCandle,
    AsyncCexTicker,
    AsyncCexFee,
    AsyncCexWalletStatus,
    AsyncCexAnnouncement,
    AsyncCexToken,
    AsyncCexSymbol,
)
from datamaxi.aio.funding_rate import AsyncFundingRate
from datamaxi.aio.forex import AsyncForex
from datamaxi.aio.premium import AsyncPremium
from datamaxi.aio.liquidation import AsyncLiquidation
from datamaxi.aio.open_interest import AsyncOpenInterest
from datamaxi.aio.margin_borrow import AsyncMarginBorrow
from datamaxi.aio.index_price import AsyncIndexPrice
from datamaxi.aio.telegram import AsyncTelegram
from datamaxi.aio.naver import AsyncNaver


class AsyncDatamaxi:
    """Async entrypoint — full mirror of the sync :class:`datamaxi.Datamaxi`.

    Use as an async context manager so the underlying ``httpx`` client is
    closed, or call :meth:`aclose` explicitly.
    """

    def __init__(self, api_key=None, **kwargs: Any):
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        api = AsyncAPI(api_key, **kwargs)
        self._api = api

        self.cex = AsyncCex(api)
        self.funding_rate = AsyncFundingRate(api)
        self.forex = AsyncForex(api)
        self.premium = AsyncPremium(api)
        self.liquidation = AsyncLiquidation(api)
        self.open_interest = AsyncOpenInterest(api)
        self.margin_borrow = AsyncMarginBorrow(api)
        self.index_price = AsyncIndexPrice(api)
        self.telegram = AsyncTelegram(api=api)
        self.naver = AsyncNaver(api=api)

    async def aclose(self):
        await self._api.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    def __repr__(self):
        return "AsyncDatamaxi(base_url={!r}, has_key={})".format(
            self._api.base_url, bool(self._api.api_key)
        )


__all__ = [
    "AsyncDatamaxi",
    "AsyncTelegram",
    "AsyncNaver",
    "AsyncAPI",
    "AsyncResource",
    "AsyncCex",
    "AsyncCexCandle",
    "AsyncCexTicker",
    "AsyncCexFee",
    "AsyncCexWalletStatus",
    "AsyncCexAnnouncement",
    "AsyncCexToken",
    "AsyncCexSymbol",
    "AsyncFundingRate",
    "AsyncForex",
    "AsyncPremium",
    "AsyncLiquidation",
    "AsyncOpenInterest",
    "AsyncMarginBorrow",
    "AsyncIndexPrice",
]
