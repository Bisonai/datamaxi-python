from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.constants import BASE_URL
from datamaxi.lib.utils import postprocess


class Naver(API):
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

        `GET /v1/naver/symbols`

        <https://docs.datamaxi.finance/api/datasets/trend/naver/symbols>

        Returns:
            List of supported Naver trend token symbols
        """
        url_path = "/v1/naver/symbols"
        return self.query(url_path)

    @postprocess()
    def trend(self, symbol: str, pandas: bool = True) -> Union[List, pd.DataFrame]:
        """Get Naver trend for given token symbol

        `GET /v1/naver/trend`

        <https://docs.datamaxiplus.com/api/datasets/trend/naver/trend>

        Args:
            symbol (str): token symbol to search for
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Naver trend data
        """
        check_required_parameter(symbol, "symbol")
        params = {"symbol": symbol}
        return self.query("/v1/naver/trend", params)
