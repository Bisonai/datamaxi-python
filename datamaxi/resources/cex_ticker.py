from __future__ import annotations

from typing import Any, List, Union, Optional, TYPE_CHECKING
from datamaxi.api import Resource
from datamaxi.lib.utils import check_required_parameters
from datamaxi.resources.utils import to_indexed_dataframe
from datamaxi.resources.responses import TickerResponse
from datamaxi.lib.constants import SPOT, FUTURES, Market

if TYPE_CHECKING:
    import pandas as pd


class CexTicker(Resource):
    """Client to fetch ticker data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize cex ticker client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def get(
        self,
        exchange: str,
        symbol: str,
        market: Market,
        currency: Optional[str] = None,
        conversion_base: Optional[str] = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, TickerResponse]:
        """Fetch ticker data

        `GET /api/v1/ticker`

        <https://docs.datamaxiplus.com/rest/cex/ticker/data>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            market (str): Market type (spot/futures)
            currency (str): Price currency
            conversion_base (str): Conversion base currency
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Ticker data in pandas DataFrame or dict response
        """

        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [market, "market"],
            ]
        )

        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        res = self.request_endpoint(
            "ticker",
            exchange=exchange,
            symbol=symbol,
            market=market,
            currency=currency,
            conversion_base=conversion_base,
        )

        if pandas:
            return to_indexed_dataframe([res["data"]], "d")
        else:
            return res

    def exchanges(
        self,
        market: Market,
    ) -> List[str]:
        """Fetch supported exchanges for ticker data.

        `GET /api/v1/ticker/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/ticker/exchanges>

        Args:
            market (str): Market type (spot/futures)

        Returns:
            List of supported exchanges
        """
        check_required_parameters(
            [
                [market, "market"],
            ]
        )

        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        return self.request_endpoint("ticker_exchanges", market=market)

    def symbols(
        self,
        exchange: str,
        market: Market,
    ) -> List[str]:
        """Fetch supported symbols for ticker data.

        `GET /api/v1/ticker/symbols`

        <https://docs.datamaxiplus.com/rest/cex/ticker/symbols>

        Args:
            exchange (str): Exchange name
            market (str): Market type (spot/futures)

        Returns:
            List of supported symbols
        """
        check_required_parameters(
            [
                [exchange, "exchange"],
                [market, "market"],
            ]
        )

        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        return self.request_endpoint("ticker_symbols", exchange=exchange, market=market)
