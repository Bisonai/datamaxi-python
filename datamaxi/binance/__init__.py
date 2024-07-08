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

    @postprocess()
    def funding_rate(
        self,
        symbol: str,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get Binance funding rate data

        `GET /v1/raw/binance/funding-rate`

        <https://docs.datamaxiplus.com/api/datasets/cex-raw/binance/funding-rate>

        Args:
            symbol (str): Binance symbol
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Binance funding rate data for a given symbol in pandas DataFrame
        """
        check_required_parameters([[symbol, "symbol"]])

        params = {"symbol": symbol}
        return self.query("/v1/raw/binance/funding-rate", params)
