from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.constants import SPOT, FUTURES, Market


class CexTicker(API):
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
        currency: str = None,
        conversion_base: str = None,
        include_source: bool = False,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch ticker data

        `GET /api/v1/ticker`

        <https://docs.datamaxiplus.com/rest/cex/ticker/data>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            market (str): Market type (spot/futures)
            currency (str): Price currency
            conversion_base (str): Conversion base currency
            include_source (bool): Include the frame's transport source
                (``ws``|``rest``) in the response
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
            include_source=include_source,
        )

        if pandas:
            df = pd.DataFrame([res["data"]])
            df = df.set_index("d")
            return df
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
