from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import check_required_parameter


class Ticker(API):
    """Client to fetch ticker data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize ticker client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def get(
        self,
        exchange: str,
        symbol: str,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch ticker data

        `GET /api/v1/ticker`

        <https://docs.datamaxiplus.com/api/datasets/ticker/ticker>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Ticker data in pandas DataFrame
        """

        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
            ]
        )

        params = {
            "exchange": exchange,
            "symbol": symbol,
        }

        res = self.query("/api/v1/ticker", params)

        if pandas:
            df = pd.DataFrame(res)
            df = df.set_index("d")
            return df
        else:
            return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.Ticker.get](./#datamaxi.datamaxi.Ticker.get)
        API.

        `GET /api/v1/ticker/exchanges`

        <https://docs.datamaxiplus.com/api/datasets/ticker/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/ticker/exchanges"
        return self.query(url_path)

    def symbols(self, exchange: str) -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.Ticker.get](./#datamaxi.datamaxi.Ticker.get)
        API.

        `GET /api/v1/ticker/symbols`

        <https://docs.datamaxiplus.com/api/datasets/ticker/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")

        params = {
            "exchange": exchange,
        }

        url_path = "/api/v1/ticker/symbols"
        return self.query(url_path, params)
