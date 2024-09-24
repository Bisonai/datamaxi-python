from typing import Any
from datamaxi.datamaxi.cex_candle import CexCandle


class Cex:
    """Client to fetch CEX data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize candle client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        self.candle = CexCandle(api_key, **kwargs)
