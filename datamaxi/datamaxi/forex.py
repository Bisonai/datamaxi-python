from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter


class Forex(API):
    """Client to fetch forex data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize forex client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

        self.__module__ = __name__
        self.__qualname__ = self.__class__.__qualname__

    def __call__(
        self,
        symbol: str,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch forex data

        `GET /api/v1/forex`

        <https://docs.datamaxiplus.com/rest/forex/forex>

        Args:
            symbol (str): Symbol name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Forex data in pandas DataFrame
        """
        check_required_parameter(symbol, "symbol")

        params = {
            "symbol": symbol,
        }

        res = self.query("/api/v1/forex", params)

        if pandas:
            return pd.DataFrame([res])
        else:
            return res

    def symbols(self) -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.Forex.get](./#datamaxi.datamaxi.Forex.get)
        API.

        `GET /api/v1/forex/symbols`

        <https://docs.datamaxiplus.com/rest/forex/symbols>

        Returns:
            List of supported symbols
        """
        url_path = "/api/v1/forex/symbols"
        return self.query(url_path)
