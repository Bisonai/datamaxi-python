from typing import Any

from datamaxi.lib.constants import BASE_URL
from datamaxi.aio._core import AsyncAPI
from datamaxi.aio.cex import AsyncCex
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
