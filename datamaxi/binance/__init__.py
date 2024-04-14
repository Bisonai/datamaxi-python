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
        """Supported Binance supported symbols

        `GET /v1/raw/binance/symbols`

        <https://docs.neverest.finance/cex/binance/symbols>

        Returns:
            List of supported Binance symbols
        """
        url_path = "/v1/raw/binance/symbols"
        return self.query(url_path)

    @postprocess()
    def kline(
        self, symbol: str, interval: str = "1d", pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get Binance k-line data

        `GET /v1/raw/binance/kline`

        <https://docs.neverest.finance/cex/binance/kline>

        Args:
            symbol (str): Binance symbol
            interval (str): Kline interval
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Binance kline data for a given symbol and interval in pandas DataFrame
        """
        check_required_parameters([[symbol, "symbol"], [interval, "interval"]])
        params = {"symbol": symbol, "interval": interval}
        return self.query("/v1/raw/binance/kline", params)
