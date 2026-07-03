"""Async margin-borrow resource — mirror of ``datamaxi.resources.margin_borrow``."""

from typing import Any, Dict

from datamaxi.aio._core import AsyncResource
from datamaxi.lib.utils import check_required_parameter


class AsyncMarginBorrow(AsyncResource):
    async def __call__(self, asset: str) -> Dict[str, Any]:
        check_required_parameter(asset, "asset")
        return await self.request_endpoint("margin_borrow", asset=asset)
