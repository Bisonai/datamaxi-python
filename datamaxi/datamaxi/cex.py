from typing import Any
from datamaxi.datamaxi.cex_candle import CexCandle
from datamaxi.datamaxi.cex_ticker import CexTicker
from datamaxi.datamaxi.cex_orderbook import CexOrderbook
from datamaxi.datamaxi.cex_trading_fees import CexTradingFees
from datamaxi.datamaxi.cex_wallet_status import CexWalletStatus
from datamaxi.datamaxi.cex_announcement import CexAnnouncement
from datamaxi.datamaxi.cex_token_updates import CexTokenUpdates


class Cex:
    """Client to fetch CEX data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize candle client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        self.candle = CexCandle(api_key, **kwargs)
        self.ticker = CexTicker(api_key, **kwargs)
        self.orderbook = CexOrderbook(api_key, **kwargs)
        self.trading_fees = CexTradingFees(api_key, **kwargs)
        self.wallet_status = CexWalletStatus(api_key, **kwargs)
        self.announcements = CexAnnouncement(api_key, **kwargs)
        self.token_updates = CexTokenUpdates(api_key, **kwargs)
