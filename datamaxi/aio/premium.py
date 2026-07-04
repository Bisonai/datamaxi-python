"""Async premium resource — mirror of ``datamaxi.resources.premium``."""

from __future__ import annotations

from typing import List, Union, Optional, TYPE_CHECKING

from datamaxi.aio._core import AsyncResource
from datamaxi.resources.responses import PremiumResponse
from datamaxi.lib.constants import Market, SortOrder

if TYPE_CHECKING:
    import pandas as pd


class AsyncPremium(AsyncResource):
    async def __call__(  # noqa: C901
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
        params = {}

        if source_exchange is not None:
            params["source_exchange"] = source_exchange

        if target_exchange is not None:
            params["target_exchange"] = target_exchange

        if asset is not None:
            params["asset"] = asset

        if source_quote is not None:
            params["source_quote"] = source_quote

        if target_quote is not None:
            params["target_quote"] = target_quote

        if sort is not None:
            params["sort"] = sort

        if key is not None:
            params["key"] = key

        if query is not None:
            params["query"] = query

        if page is not None:
            params["page"] = page

        if limit is not None:
            params["limit"] = limit

        if currency is not None:
            params["currency"] = currency

        if conversion_base is not None:
            params["conversion_base"] = conversion_base

        if min_sv is not None:
            params["min_sv"] = min_sv

        if min_tv is not None:
            params["min_tv"] = min_tv

        if source_market is not None:
            params["source_market"] = source_market

        if target_market is not None:
            params["target_market"] = target_market

        if only_transferable:
            params["only_transferable"] = True

        if network is not None:
            params["network"] = network

        if premium_type is not None:
            params["premium_type"] = premium_type

        if token_include is not None:
            params["token_include"] = token_include

        if token_exclude is not None:
            params["token_exclude"] = token_exclude

        res = await self.request_endpoint("premium", **params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        if pandas:
            import pandas as pd

            df = pd.DataFrame(
                [
                    {
                        **item["detail"],
                        "source_annualized_funding_rate": item.get(
                            "source_annualized_funding_rate"
                        ),
                        "target_annualized_funding_rate": item.get(
                            "target_annualized_funding_rate"
                        ),
                    }
                    for item in res["data"]
                ]
            )
            return df
        return res

    async def exchanges(self) -> List[str]:
        return await self.request_endpoint("premium_exchanges")
