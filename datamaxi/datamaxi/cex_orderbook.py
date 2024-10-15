from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import check_required_parameter


class CexOrderbook(API):
    """Client to fetch orderbook data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize orderbook client.

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
        """Fetch orderbook data

        `GET /api/v1/orderbook`

        <https://docs.datamaxiplus.com/rest/cex/orderbook/data>

        Args:
            exchange (str): Exchange name
            symbol (str): symbol name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            CexOrderbook data in pandas DataFrame
        """

        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
            ]
        )

        params = {"exchange": exchange, "symbol": symbol}

        res = self.query("/api/v1/orderbook", params)
        if pandas:
            df = pd.DataFrame(res)
            df = df.set_index("d")
            return df

        return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.CexOrderbook.get](./#datamaxi.datamaxi.CexOrderbook.get)
        API.

        `GET /api/v1/orderbook/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/orderbook/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/orderbook/exchanges"
        return self.query(url_path)

    def symbols(self, exchange: str) -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.CexOrderbook.get](./#datamaxi.datamaxi.CexOrderbook.get)
        API.

        `GET /api/v1/orderbook/symbols`

        <https://docs.datamaxiplus.com/rest/cex/orderbook/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")

        params = {
            "exchange": exchange,
        }

        url_path = "/api/v1/orderbook/symbols"
        return self.query(url_path, params)
