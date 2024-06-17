from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import postprocess
from datamaxi.lib.constants import BASE_URL


class Gopax(API):
    """Client to fetch Gopax data from DataMaxi+ API."""

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
        """Gopax supported symbols

        `GET /v1/raw/gopax/symbols`

        <https://docs.datamaxiplus.com/api/datasets/cex-raw/gopax/symbols>

        Returns:
            List of supported Gopax symbols
        """
        url_path = "/v1/raw/gopax/symbols"
        return self.query(url_path)

    def intervals(self) -> List[str]:
        """Gopax supported intervals

        `GET /v1/raw/gopax/intervals`

        <https://docs.datamaxiplus.com/api/datasets/cex-raw/gopax/intervals>

        Returns:
            List of supported Gopax intervals
        """
        url_path = "/v1/raw/gopax/intervals"
        return self.query(url_path)

    @postprocess()
    def candle(
        self, symbol: str, interval: str = "1d", pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get Gopax candle data

        `GET /v1/raw/gopax/candle`

        <https://docs.datamaxiplus.com/api/datasets/cex-raw/gopax/candle>

        Args:
            symbol (str): Gopax symbol
            interval (str): Candle interval
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Gopax candle data for a given symbol and interval in pandas DataFrame
        """
        check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
        params = {"symbol": symbol, "interval": interval}
        return self.query("/v1/raw/gopax/candle", params)
