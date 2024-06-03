from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import postprocess
from datamaxi.lib.constants import BASE_URL


class Upbit(API):
    """Client to fetch Upbit data from DataMaxi+ API."""

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
        """Upbit supported symbols

        `GET /v1/raw/upbit/symbols`

        <https://docs.datamaxiplus.com/cex/upbit/symbols>

        Returns:
            List of supported Upbit symbols
        """
        url_path = "/v1/raw/upbit/symbols"
        return self.query(url_path)

    def intervals(self) -> List[str]:
        """Upbit supported intervals

        `GET /v1/raw/upbit/intervals`

        <https://docs.datamaxiplus.com/cex/upbit/intervals>

        Returns:
            List of supported Upbit intervals
        """
        url_path = "/v1/raw/upbit/intervals"
        return self.query(url_path)

    @postprocess()
    def candle(
        self, symbol: str, interval: str = "1d", pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get Upbit candle data

        `GET /v1/raw/upbit/candle`

        <https://docs.datamaxiplus.com/cex/upbit/candle>

        Args:
            symbol (str): Upbit symbol
            interval (str): Candle interval
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Upbit candle data for a given symbol and interval in pandas DataFrame
        """
        check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
        params = {"symbol": symbol, "interval": interval}
        return self.query("/v1/raw/upbit/candle", params)
