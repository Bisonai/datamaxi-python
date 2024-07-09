from typing import Any, Callable, Dict, Tuple, Union
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

    def funding_rate(
        self,
        symbol: str,
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: str = "desc",
        pandas: bool = True,
    ) -> Union[Tuple[Dict, Callable], Tuple[pd.DataFrame, Callable]]:
        """Get Binance funding rate data

        `GET /v1/raw/binance/funding-rate`

        <https://docs.datamaxiplus.com/api/datasets/cex-raw/binance/funding-rate>

        Args:
            symbol (str): Binance symbol
            page (int): Page number
            limit (int): Limit of data
            fromDateTime (str): Start date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            toDateTime (str): End date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            sort (str): Sort order
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Binance funding rate data for a given symbol in pandas DataFrame and next request function
        """
        check_required_parameters([[symbol, "symbol"]])

        params = {
            "symbol": symbol,
            "page": page,
            "limit": limit,
            "fromDateTime": fromDateTime,
            "toDateTime": toDateTime,
            "sort": sort,
        }

        res = self.query("/v1/raw/binance/funding-rate", params)
        if res["data"] is None:
            raise ValueError("no data found")

        next_request = lambda: self.funding_rate(
            symbol,
            page + 1,
            limit,
            fromDateTime,
            toDateTime,
            sort,
            pandas,
        )

        if pandas:
            df = pd.DataFrame(res["data"])
            df = df.set_index("d")
            df.replace("NaN", pd.NA, inplace=True)
            df = df.apply(pd.to_numeric, errors="coerce")
            return df, next_request
        else:
            return res, next_request
