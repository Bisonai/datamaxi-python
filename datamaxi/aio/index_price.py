"""Async index-price resource — mirror of ``datamaxi.resources.index_price``."""

from typing import Any, Dict, Optional

from datamaxi.aio._core import AsyncResource
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.constants import Interval


class AsyncIndexPrice(AsyncResource):
    async def __call__(
        self,
        asset: str,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        interval: Interval = "5m",
    ) -> Dict[str, Any]:
        check_required_parameter(asset, "asset")
        return await self.request_endpoint(
            "index_price",
            asset=asset,
            interval=interval,
            **{"from": from_, "to": to},
        )
