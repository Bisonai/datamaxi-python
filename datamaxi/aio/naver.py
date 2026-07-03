"""Async Naver client — mirror of ``datamaxi.naver.Naver``.

Standalone top-level async client (builds its own ``AsyncAPI``). Use as an
async context manager so the underlying httpx client is closed.
"""

from __future__ import annotations

from typing import Any, List, Union, TYPE_CHECKING

from datamaxi.aio._core import AsyncAPI, AsyncResource
from datamaxi.resources.responses import NaverTrendRow
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.constants import BASE_URL

if TYPE_CHECKING:
    import pandas as pd


class AsyncNaver(AsyncResource):
    """Client to fetch Naver trend data from DataMaxi+ API (async)."""

    def __init__(self, api_key=None, **kwargs: Any):
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(AsyncAPI(api_key, **kwargs))

    async def aclose(self):
        await self._api.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    def __repr__(self):
        return "AsyncNaver(base_url={!r}, has_key={})".format(
            self._api.base_url, bool(self._api.api_key)
        )

    async def symbols(self) -> List[str]:
        return await self.request_endpoint("naver_trend_symbols")

    async def trend(
        self, symbol: str, pandas: bool = True
    ) -> Union[pd.DataFrame, List[NaverTrendRow]]:
        check_required_parameter(symbol, "symbol")
        res = await self.request_endpoint("naver_trend", symbol=symbol)
        if pandas:
            import pandas as pd

            return pd.DataFrame(res)
        return res
