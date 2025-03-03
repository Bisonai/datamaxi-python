from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.constants import SPOT, FUTURES


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
        market: str,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch ticker data

        `GET /api/v1/ticker`

        <https://docs.datamaxiplus.com/rest/cex/ticker/data>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            market (str): Market type (spot/futures)
            pandas (bool): Return data as pandas DataFrame

        Returns:
            CexTicker data in pandas DataFrame
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

        params = {
            "exchange": exchange,
            "symbol": symbol,
            "market": market,
        }

        res = self.query("/api/v1/ticker", params)

        if pandas:
            df = pd.DataFrame(res)
            df = df.set_index("d")
            return df
        else:
            return res

    def exchanges(
        self,
        market: str,
    ) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.CexTicker.get](./#datamaxi.datamaxi.CexTicker.get)
        API.

        `GET /api/v1/ticker/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/ticker/exchanges>

        Args:
            market (str): Market type (spot/futures)

        Returns:
            List of supported exchange
        """
        check_required_parameters(
            [
                [market, "market"],
            ]
        )

        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        params = {
            "market": market,
        }

        url_path = "/api/v1/ticker/exchanges"
        return self.query(url_path, params)

    def symbols(
        self,
        exchange: str,
        market: str,
    ) -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.CexTicker.get](./#datamaxi.datamaxi.CexTicker.get)
        API.

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

        params = {
            "exchange": exchange,
            "market": market,
        }

        url_path = "/api/v1/ticker/symbols"
        return self.query(url_path, params)
