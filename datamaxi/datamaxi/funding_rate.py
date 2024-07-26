from typing import Any, Callable, Tuple, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.datamaxi.utils import convert_data_to_data_frame


class FundingRate(API):
    """Client to fetch funding rate data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize funding rate client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def get(
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
        """Fetch funding rate data

        `GET /api/v1/funding-rate`

        <https://docs.datamaxiplus.com/api/datasets/funding-rate/funding-rate>

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
            Funding rate data in pandas DataFrame and next request function
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

        res = self.query("/api/v1/funding-rate", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.get(
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
            df = convert_data_to_data_frame(res["data"])
            return df, next_request
        else:
            return res, next_request

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.FundingRate.get](./#datamaxi.datamaxi.FundingRate.get)
        API.

        `GET /api/v1/funding-rate/exchanges`

        <https://docs.datamaxiplus.com/api/datasets/funding-rate/exchanges>

        Returns:
            List of supported exchanges
        """
        url_path = "/api/v1/funding-rate/exchanges"
        return self.query(url_path)

    def symbols(self, exchange: str, market: str = "spot") -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.FundingRate.get](./#datamaxi.datamaxi.FundingRate.get)
        API.

        `GET /api/v1/funding-rate/symbols`

        <https://docs.datamaxiplus.com/api/datasets/funding-rate/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")
        params = {"exchange": exchange}
        url_path = "/api/v1/funding-rate/symbols"
        return self.query(url_path, params)
