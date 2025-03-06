from typing import Any, List, Dict
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter


class CexFee(API):
    """Client to fetch CEX trading fee data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize trading fee client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def __call__(
        self,
        exchange: str = None,
        symbol: str = None,
    ) -> List[Dict]:
        """Fetch trading fee data

        `GET /api/v1/trading-fees`

        <https://docs.datamaxiplus.com/rest/cex/trading-fees/data>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name

        Returns:
            Trading fee data
        """
        params = {}
        if exchange:
            params["exchange"] = exchange
        if symbol:
            params["symbol"] = symbol

        url_path = "/api/v1/cex/fees"
        return self.query(url_path, params)

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.CexFee.get](./#datamaxi.datamaxi.CexFee.get)
        API.

        `GET /api/v1/trading-fees/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/trading-fees/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/cex/fees/exchanges"
        return self.query(url_path)

    def symbols(self, exchange: str) -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.CexTradingFees.get](./#datamaxi.datamaxi.CexTradingFees.get)
        API.

        `GET /api/v1/trading-fees/symbols`

        <https://docs.datamaxiplus.com/rest/cex/trading-fees/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported assets
        """
        check_required_parameter(exchange, "exchange")

        params = {
            "exchange": exchange,
        }

        url_path = "/api/v1/cex/fees/symbols"
        return self.query(url_path, params)
