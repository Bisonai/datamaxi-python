from __future__ import annotations

from typing import Any, Callable, Tuple, List, Union, TYPE_CHECKING
from datamaxi.api import Resource
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.resources.utils import convert_data_to_data_frame
from datamaxi.resources.responses import FundingHistoryResponse, LatestFundingRate
from datamaxi.lib.constants import ASC, DESC, SortOrder

if TYPE_CHECKING:
    import pandas as pd


class FundingRate(Resource):
    """Client to fetch funding rate data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize funding rate client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def history(
        self,
        exchange: str,
        symbol: str,
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: SortOrder = DESC,
        pandas: bool = True,
    ) -> Union[Tuple[pd.DataFrame, Callable], Tuple[FundingHistoryResponse, Callable]]:
        """Fetch historical funding rate data

        `GET /api/v1/funding-rate/history`

        <https://docs.datamaxiplus.com/rest/cex/funding-rate/historical-funding-rate>

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
            Historical funding rate data in pandas DataFrame and next request function
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

        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        res = self.request_endpoint(
            "funding_rate_history",
            exchange=exchange,
            symbol=symbol,
            page=page,
            limit=limit,
            sort=sort,
            **{"from": fromDateTime, "to": toDateTime},
        )
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        def next_request():
            return self.history(
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

    def latest(
        self,
        exchange: str = None,
        symbol: str = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, LatestFundingRate]:
        """Fetch latest funding rate data

        `GET /api/v1/funding-rate/latest`

        <https://docs.datamaxiplus.com/rest/cex/funding-rate/latest-funding-rate>

        Args:
            exchange (str): exchange name
            symbol (str): Symbol name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Latest funding rate data in pandas DataFrame or dict response
        """
        res = self.request_endpoint(
            "funding_rate_latest", exchange=exchange, symbol=symbol
        )

        if pandas:
            import pandas as pd

            df = pd.DataFrame([res])
            df = df.set_index("d")
            return df
        else:
            return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges for funding rate endpoints.

        `GET /api/v1/funding-rate/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/funding-rate/exchanges>

        Returns:
            List of supported exchanges
        """
        return self.request_endpoint("funding_rate_exchanges")

    def symbols(self, exchange: str) -> List[str]:
        """Fetch supported symbols for funding rate endpoints.

        `GET /api/v1/funding-rate/symbols`

        <https://docs.datamaxiplus.com/rest/cex/funding-rate/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")
        return self.request_endpoint("funding_rate_symbols", exchange=exchange)
