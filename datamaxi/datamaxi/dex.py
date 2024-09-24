from typing import Any
from datamaxi.datamaxi.dex_trade import DexTrade
from datamaxi.datamaxi.dex_candle import DexCandle


class Dex:
    """Client to fetch DEX data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize candle client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        self.candle = DexCandle(api_key, **kwargs)
        self.trade = DexTrade(api_key, **kwargs)
