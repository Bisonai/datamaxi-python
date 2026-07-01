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

        `GET /api/v1/cex/fees`

        <https://docs.datamaxiplus.com/rest/cex/trading-fees/data>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name

        Returns:
            Trading fee data
        """
        return self.request_endpoint("cex_fees", exchange=exchange, symbol=symbol)

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges for fee data.

        `GET /api/v1/cex/fees/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/trading-fees/exchanges>

        Returns:
            List of supported exchanges
        """
        return self.request_endpoint("cex_fees_exchanges")

    def symbols(self, exchange: str) -> List[str]:
        """Fetch supported symbols for fee data.

        `GET /api/v1/cex/fees/symbols`

        <https://docs.datamaxiplus.com/rest/cex/trading-fees/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")

        return self.request_endpoint("cex_fees_symbols", exchange=exchange)
