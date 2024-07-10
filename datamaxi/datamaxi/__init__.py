from typing import Any, Callable, Tuple, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.constants import BASE_URL


class Datamaxi(API):
    """Client to fetch unified data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL

        super().__init__(api_key, **kwargs)

    def symbols(self, exchange: str) -> List[str]:
        """Supported symbols by given exchange

        `GET /v1/symbols`

        <https://docs.datamaxiplus.com/api/datasets/cex/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")
        params = {"exchange": exchange}
        url_path = "/v1/symbols"
        return self.query(url_path, params)

    def intervals(self, exchange: str) -> List[str]:
        """Supported intervals by given exchange

        `GET /v1/intervals`

        <https://docs.datamaxiplus.com/api/datasets/cex/intervals>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported intervals
        """
        check_required_parameter(exchange, "exchange")
        params = {"exchange": exchange}
        url_path = "/v1/intervals"
        return self.query(url_path, params)

    def candle(
        self,
        exchange: str,
        symbol: str,
        interval: str = "1d",
        market: str = "spot",
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: str = "desc",
        pandas: bool = True,
    ) -> Union[Tuple[Dict, Callable], Tuple[pd.DataFrame, Callable]]:
        """Get candle data

        `GET /v1/candle`

        <https://docs.datamaxiplus.com/api/datasets/cex/candle>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            interval (str): Candle interval
            market (str): Market type (spot/futures)
            page (int): Page number
            limit (int): Limit of data
            fromDateTime (str): Start date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            toDateTime (str): End date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            sort (str): Sort order
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Candle data for a given symbol, interval and market in pandas DataFrame and next request function
        """
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [interval, "interval"],
                [market, "market"],
            ]
        )

        if market not in ["spot", "futures"]:
            raise ValueError("market must be either spot or futures")

        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if fromDateTime is not None and toDateTime is not None:
            raise ValueError(
                "fromDateTime and toDateTime cannot be set at the same time"
            )

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "exchange": exchange,
            "symbol": symbol,
            "interval": interval,
            "market": market,
            "page": page,
            "limit": limit,
            "fromDateTime": fromDateTime,
            "toDateTime": toDateTime,
            "sort": sort,
        }

        res = self.query("/v1/candle", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.candle(
                exchange,
                symbol,
                interval,
                market,
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

    def funding_rate(
        self,
        exchange: str,
        symbol: str,
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: str = "desc",
        pandas: bool = True,
    ) -> Union[Tuple[Dict, Callable], Tuple[pd.DataFrame, Callable]]:
        """Get funding rate data

        `GET /v1/funding-rate`

        <https://docs.datamaxiplus.com/api/datasets/cex/funding-rate>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            page (int): Page number
            limit (int): Limit of data
            fromDateTime (str): Start date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            toDateTime (str): End date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            sort (str): Sort order
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Funding rate data for a given symbol and exchange in pandas DataFrame and next request function
        """
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
            ]
        )

        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if fromDateTime is not None and toDateTime is not None:
            raise ValueError(
                "fromDateTime and toDateTime cannot be set at the same time"
            )

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "exchange": exchange,
            "symbol": symbol,
            "page": page,
            "limit": limit,
            "fromDateTime": fromDateTime,
            "toDateTime": toDateTime,
            "sort": sort,
        }

        res = self.query("/v1/funding-rate", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.funding_rate(
                exchange,
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
