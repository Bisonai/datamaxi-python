from typing import Any, Callable, Tuple, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.datamaxi.utils import convert_data_to_data_frame


class CexCandle(API):
    """Client to fetch CEX candle data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def get(
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
        """Fetch candle data

        `GET /api/v1/cex/candle`

        <https://docs.datamaxiplus.com/rest/cex/candle/data>

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
            Candle data in pandas DataFrame and next request function
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
            "from": fromDateTime,
            "to": toDateTime,
            "sort": sort,
        }

        res = self.query("/api/v1/cex/candle", params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        def next_request():
            return self.get(
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
            df = convert_data_to_data_frame(res["data"])
            return df, next_request
        else:
            return res, next_request

    def exchanges(self, market: str = "spot") -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.CexCandle.get](./#datamaxi.datamaxi.CexCandle.get)
        API.

        `GET /api/v1/cex/candle/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/candle/exchanges>

        Args:
            market (str): Market type (spot/futures)

        Returns:
            List of supported exchanges
        """
        check_required_parameter(market, "market")

        if market not in ["spot", "futures"]:
            raise ValueError("market must be either spot or futures")

        params = {"market": market}
        url_path = "/api/v1/cex/candle/exchanges"
        return self.query(url_path, params)

    def symbols(self, exchange: str = None, market: str = None) -> List[Dict]:
        """Fetch supported symbols accepted by
        [datamaxi.CexCandle.get](./#datamaxi.datamaxi.CexCandle.get)
        API.

        `GET /api/v1/cex/candle/symbols`

        <https://docs.datamaxiplus.com/rest/cex/candle/symbols>

        Args:
            exchange (str): Exchange name
            market (str): Market type (spot/futures)

        Returns:
            List of supported symbols
        """
        if market is not None and market not in ["spot", "futures"]:
            raise ValueError("market must be either spot or futures")

        params = {}
        if exchange is not None:
            params["exchange"] = exchange
        if market is not None:
            params["market"] = market

        url_path = "/api/v1/cex/candle/symbols"
        return self.query(url_path, params)

    def intervals(self) -> List[str]:
        """Fetch supported intervals accepted by
        [datamaxi.CexCandle.get](./#datamaxi.datamaxi.CexCandle.get)
        API.

        `GET /api/v1/candle/intervals`

        <https://docs.datamaxiplus.com/rest/cex/candle/intervals>

        Returns:
            List of supported intervals
        """
        url_path = "/api/v1/cex/candle/intervals"
        return self.query(url_path)
