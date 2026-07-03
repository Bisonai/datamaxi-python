"""Async liquidation resource — mirror of ``datamaxi.resources.liquidation``."""

from typing import Any, Dict, Optional

from datamaxi.aio._core import AsyncResource
from datamaxi.lib.constants import Interval


class AsyncLiquidation(AsyncResource):
    async def __call__(
        self,
        exchange: str,
        symbol: str,
        limit: int = 100,
    ) -> Dict[str, Any]:
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        return await self.request_endpoint(
            "liquidation", exchange=exchange, symbol=symbol, limit=limit
        )

    async def feed(
        self,
        limit: int = 100,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        min_volume_usd: Optional[float] = None,
    ) -> Dict[str, Any]:
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        return await self.request_endpoint(
            "liquidation_feed",
            limit=limit,
            exchange=exchange,
            base=base,
            min_volume_usd=min_volume_usd,
        )

    async def heatmap(
        self,
        window: str = "1h",
        topN: int = 10,
    ) -> Dict[str, Any]:
        if topN < 1 or topN > 30:
            raise ValueError("topN must be between 1 and 30")
        return await self.request_endpoint(
            "liquidation_heatmap", window=window, top_n=topN
        )

    async def map(
        self,
        base: str,
        exchange: str = "binance",
        quote: str = "USDT",
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "liquidation_map", base=base, exchange=exchange, quote=quote
        )

    async def stats(
        self,
        window: str = "1h",
        exchange: Optional[str] = None,
        min_volume_usd: Optional[float] = None,
    ) -> Dict[str, Any]:
        if window not in ("1h", "4h", "24h"):
            raise ValueError("window must be one of 1h, 4h, or 24h")
        return await self.request_endpoint(
            "liquidation_stats",
            window=window,
            exchange=exchange,
            min_volume_usd=min_volume_usd,
        )

    async def symbol_history(
        self,
        symbol: str,
        quote: str = "USDT",
        exchange: Optional[str] = None,
        interval: Interval = "5m",
        window: str = "24h",
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "liquidation_symbol_history",
            symbol=symbol,
            quote=quote,
            exchange=exchange,
            interval=interval,
            window=window,
        )
