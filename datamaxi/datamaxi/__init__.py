from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import postprocess
from datamaxi.lib.constants import BASE_URL


class Datamaxi(API):
    """Client to fetch unified data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL

        super().__init__(api_key, **kwargs)

    def symbols(self, exchange: str) -> List[str]:
        """Supported symbols by given exchange

        `GET /v1/symbols`

        <https://docs.datamaxiplus.com/api/datasets/cex/symbols>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameter(exchange, "exchange")
        params = {"exchange": exchange}
        url_path = "/v1/symbols"
        return self.query(url_path, params)

    def intervals(self, exchange: str) -> List[str]:
        """Supported intervals by given exchange

        `GET /v1/intervals`

        <https://docs.datamaxiplus.com/api/datasets/cex/intervals>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported intervals
        """
        check_required_parameter(exchange, "exchange")
        params = {"exchange": exchange}
        url_path = "/v1/intervals"
        return self.query(url_path, params)

    @postprocess()
    def candle(
        self,
        exchange: str,
        symbol: str,
        interval: str = "1d",
        market: str = "spot",
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get candle data

        `GET /v1/candle`

        <https://docs.datamaxiplus.com/api/datasets/cex/candle>

        Args:
            exchange (str): Exchange name
            symbol (str): Symbol name
            interval (str): Candle interval
            market (str): Market type (spot/futures)
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Candle data for a given symbol, interval and market in pandas DataFrame
        """
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [interval, "interval"],
                [market, "market"],
            ]
        )

        if market not in ["spot", "futures"]:
            raise ValueError("market must be either spot or futures")

        params = {
            "exchange": exchange,
            "symbol": symbol,
            "interval": interval,
            "market": market,
        }
        return self.query("/v1/candle", params)
