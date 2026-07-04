"""Async premium resource — mirror of ``datamaxi.resources.premium``.

Param assembly and response shaping are shared with the sync resource via
``build_premium_params`` / ``shape_premium_response`` (see #154); only the
``await`` glue differs.
"""

from __future__ import annotations

from typing import List, Union, Optional, TYPE_CHECKING

from datamaxi.aio._core import AsyncResource
from datamaxi.resources.responses import PremiumResponse
from datamaxi.resources.premium import build_premium_params, shape_premium_response
from datamaxi.lib.constants import Market, SortOrder

if TYPE_CHECKING:
    import pandas as pd


class AsyncPremium(AsyncResource):
    async def __call__(
        self,
        source_exchange: Optional[str] = None,
        target_exchange: Optional[str] = None,
        asset: Optional[str] = None,
        source_quote: Optional[str] = None,
        target_quote: Optional[str] = None,
        sort: Optional[SortOrder] = None,
        key: Optional[str] = None,
        page: int = 1,
        limit: int = 100,
        currency: Optional[str] = None,
        conversion_base: Optional[str] = None,
        min_sv: Optional[str] = None,
        min_tv: Optional[str] = None,
        source_market: Optional[Market] = None,
        target_market: Optional[Market] = None,
        only_transferable: bool = False,
        network: Optional[str] = None,
        premium_type: Optional[str] = None,
        token_include: Optional[str] = None,
        token_exclude: Optional[str] = None,
        query: Optional[str] = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, PremiumResponse]:
        params = build_premium_params(
            source_exchange=source_exchange,
            target_exchange=target_exchange,
            asset=asset,
            source_quote=source_quote,
            target_quote=target_quote,
            sort=sort,
            key=key,
            page=page,
            limit=limit,
            currency=currency,
            conversion_base=conversion_base,
            min_sv=min_sv,
            min_tv=min_tv,
            source_market=source_market,
            target_market=target_market,
            only_transferable=only_transferable,
            network=network,
            premium_type=premium_type,
            token_include=token_include,
            token_exclude=token_exclude,
            query=query,
        )
        res = await self.request_endpoint("premium", **params)
        return shape_premium_response(res, pandas)

    async def exchanges(self) -> List[str]:
        return await self.request_endpoint("premium_exchanges")
