from typing import Any, List, Dict, Union, Optional
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.datamaxi.utils import convert_data_to_data_frame
from datamaxi.lib.constants import SPOT, FUTURES, INTERVAL_1D, USD, Market, Interval


class CexCandle(API):
    """Client to fetch CEX candle data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize cex candle client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

        self.__module__ = __name__
        self.__qualname__ = self.__class__.__qualname__

    def __call__(
        self,
        exchange: str,
        market: Market,
        symbol: str,
        currency: str = USD,
        interval: Interval = INTERVAL_1D,
        from_unix: str = None,
        to_unix: str = None,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch candle data

        `GET /api/v1/cex/candle`

        <https://docs.datamaxiplus.com/rest/cex/candle/data>

        Args:
            exchange (str): Exchange name
            market (str): Market type (spot/futures)
            symbol (str): Symbol name
            currency (str): Currency
            interval (str): Candle interval
            from_unix (str): Start time in Unix timestamp
            to_unix (str): End time in Unix timestamp
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Candle data in pandas DataFrame or dict response
        """
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [interval, "interval"],
                [market, "market"],
                [currency, "currency"],
            ]
        )

        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        res = self.request_endpoint(
            "cex_candle",
            exchange=exchange,
            market=market,
            symbol=symbol,
            interval=interval,
            currency=currency,
            **{"from": from_unix, "to": to_unix},
        )
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        if pandas:
            return convert_data_to_data_frame(res["data"])
        else:
            return res

    def exchanges(self, market: Market) -> List[str]:
        """Fetch supported exchanges for candle data.

        `GET /api/v1/cex/candle/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/candle/exchanges>

        Args:
            market (str): Market type (spot/futures)

        Returns:
            List of supported exchanges
        """
        check_required_parameter(market, "market")

        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        return self.request_endpoint("cex_candle_exchanges", market=market)

    def symbols(
        self, exchange: str = None, market: Optional[Market] = None
    ) -> List[Dict]:
        """Fetch supported symbols for candle data.

        `GET /api/v1/cex/candle/symbols`

        <https://docs.datamaxiplus.com/rest/cex/candle/symbols>

        Args:
            exchange (str): Exchange name
            market (str): Market type (spot/futures)

        Returns:
            List of supported symbols
        """
        if market is not None and market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        return self.request_endpoint(
            "cex_candle_symbols", exchange=exchange, market=market
        )

    def intervals(self) -> List[str]:
        """Fetch supported intervals for candle data.

        `GET /api/v1/cex/candle/intervals`

        <https://docs.datamaxiplus.com/rest/cex/candle/intervals>

        Returns:
            List of supported intervals
        """
        return self.request_endpoint("cex_candle_intervals")
