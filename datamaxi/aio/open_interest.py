"""Async open-interest resource — mirror of ``datamaxi.resources.open_interest``."""

from typing import Any, Dict, Optional

from datamaxi.aio._core import AsyncResource
from datamaxi.lib.constants import Interval, SortOrder


class AsyncOpenInterest(AsyncResource):
    async def __call__(self, exchange: str, symbol: str) -> Dict[str, Any]:
        return await self.request_endpoint(
            "open_interest", exchange=exchange, symbol=symbol
        )

    async def list(self, exchange: Optional[str] = None) -> Dict[str, Any]:
        return await self.request_endpoint("open_interest_list", exchange=exchange)

    async def overview(
        self,
        page: int = 1,
        limit: int = 20,
        key: str = "binance",
        sort: SortOrder = "desc",
        query: Optional[str] = None,
    ) -> Dict[str, Any]:
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if sort not in ("asc", "desc"):
            raise ValueError("sort must be either asc or desc")
        return await self.request_endpoint(
            "open_interest_overview",
            page=page,
            limit=limit,
            key=key,
            sort=sort,
            query=query,
        )

    async def summary(self, topN: int = 10) -> Dict[str, Any]:
        if topN < 1 or topN > 30:
            raise ValueError("topN must be between 1 and 30")
        return await self.request_endpoint("open_interest_summary", top_n=topN)

    async def history_aggregated(
        self,
        token_id: str,
        interval: Interval = "1h",
        from_: Optional[int] = None,
        to: Optional[int] = None,
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "open_interest_history_aggregated",
            token_id=token_id,
            interval=interval,
            **{"from": from_, "to": to},
        )
