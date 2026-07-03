"""Async forex resource — mirror of ``datamaxi.resources.forex``."""

from __future__ import annotations

from typing import List, Union, TYPE_CHECKING

from datamaxi.aio._core import AsyncResource
from datamaxi.resources.responses import ForexRow
from datamaxi.lib.utils import check_required_parameter

if TYPE_CHECKING:
    import pandas as pd


class AsyncForex(AsyncResource):
    async def __call__(
        self,
        symbol: str,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, ForexRow]:
        check_required_parameter(symbol, "symbol")
        res = await self.request_endpoint("forex", symbol=symbol)
        if pandas:
            import pandas as pd

            return pd.DataFrame([res])
        return res

    async def symbols(self) -> List[str]:
        return await self.request_endpoint("forex_symbols")
