"""Async funding-rate resource — mirror of ``datamaxi.resources.funding_rate``."""

from __future__ import annotations

from typing import Callable, Tuple, List, Union, Optional, TYPE_CHECKING

from datamaxi.aio._core import AsyncResource
from datamaxi.lib.utils import check_required_parameter, check_required_parameters
from datamaxi.resources.responses import FundingHistoryResponse, LatestFundingRate
from datamaxi.lib.constants import ASC, DESC, SortOrder

if TYPE_CHECKING:
    import pandas as pd


class AsyncFundingRate(AsyncResource):
    async def history(
        self,
        exchange: str,
        symbol: str,
        page: int = 1,
        limit: int = 1000,
        fromDateTime: Optional[str] = None,
        toDateTime: Optional[str] = None,
        sort: SortOrder = DESC,
        pandas: bool = True,
    ) -> Union[Tuple[pd.DataFrame, Callable], Tuple[FundingHistoryResponse, Callable]]:
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
            ]
        )
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if fromDateTime is not None and toDateTime is not None:
            raise ValueError(
                "fromDateTime and toDateTime cannot be set at the same time"
            )
        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        res = await self.request_endpoint(
            "funding_rate_history",
            exchange=exchange,
            symbol=symbol,
            page=page,
            limit=limit,
            sort=sort,
            **{"from": fromDateTime, "to": toDateTime},
        )
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        async def next_request():
            return await self.history(
                exchange,
                symbol,
                page + 1,
                limit,
                fromDateTime,
                toDateTime,
                sort,
                pandas,
            )

        if pandas:
            from datamaxi.resources.utils import convert_data_to_data_frame

            df = convert_data_to_data_frame(res["data"])
            return df, next_request
        return res, next_request

    async def latest(
        self,
        exchange: Optional[str] = None,
        symbol: Optional[str] = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, LatestFundingRate]:
        res = await self.request_endpoint(
            "funding_rate_latest", exchange=exchange, symbol=symbol
        )
        if pandas:
            import pandas as pd

            df = pd.DataFrame([res])
            df = df.set_index("d")
            return df
        return res

    async def exchanges(self) -> List[str]:
        return await self.request_endpoint("funding_rate_exchanges")

    async def symbols(self, exchange: str) -> List[str]:
        check_required_parameter(exchange, "exchange")
        return await self.request_endpoint("funding_rate_symbols", exchange=exchange)
