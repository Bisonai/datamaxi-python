from __future__ import annotations

from typing import Any, List, Union, TYPE_CHECKING
from datamaxi.api import Resource
from datamaxi.resources.responses import NaverTrendRow
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.constants import BASE_URL

if TYPE_CHECKING:
    import pandas as pd


class Naver(Resource):
    """Client to fetch Naver trend data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def symbols(self) -> List[str]:
        """Get Naver trend supported token symbols

        `GET /api/v1/naver-trend/symbols`

        <https://docs.datamaxiplus.com/rest/trend/naver/symbols>

        Returns:
            List of supported Naver trend token symbols
        """
        return self.request_endpoint("naver_trend_symbols")

    def trend(
        self, symbol: str, pandas: bool = True
    ) -> Union[pd.DataFrame, List[NaverTrendRow]]:
        """Get Naver trend for given token symbol

        `GET /api/v1/naver-trend`

        <https://docs.datamaxiplus.com/rest/trend/naver-trend>

        Args:
            symbol (str): token symbol to search for
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Naver trend data as list or pandas DataFrame
        """
        check_required_parameter(symbol, "symbol")
        res = self.request_endpoint("naver_trend", symbol=symbol)
        if pandas:
            import pandas as pd

            return pd.DataFrame(res)
        return res
