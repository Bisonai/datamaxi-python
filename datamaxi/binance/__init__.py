from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import postprocess
from datamaxi.lib.constants import BASE_URL


class Binance(API):
    """Client to fetch Binance data from DataMaxi+ API."""

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
        """Binance supported symbols

        `GET /v1/raw/binance/symbols`

        <https://docs.datamaxiplus.com/cex/binance/symbols>

        Returns:
            List of supported Binance symbols
        """
        url_path = "/v1/raw/binance/symbols"
        return self.query(url_path)

    def intervals(self) -> List[str]:
        """Binance supported intervals

        `GET /v1/raw/binance/intervals`

        <https://docs.datamaxiplus.com/cex/binance/intervals>

        Returns:
            List of supported Binance intervals
        """
        url_path = "/v1/raw/binance/intervals"
        return self.query(url_path)

    @postprocess()
    def candle(
        self, symbol: str, interval: str = "1d", pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get Binance candle data

        `GET /v1/raw/binance/candle`

        <https://docs.datamaxiplus.com/cex/binance/candle>

        Args:
            symbol (str): Binance symbol
            interval (str): Candle interval
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Binance candle data for a given symbol and interval in pandas DataFrame
        """
        check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
        params = {"symbol": symbol, "interval": interval}
        return self.query("/v1/raw/binance/candle", params)
