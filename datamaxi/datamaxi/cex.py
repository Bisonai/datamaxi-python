from typing import Any
from datamaxi.api import API
from datamaxi.datamaxi.cex_candle import CexCandle
from datamaxi.datamaxi.cex_ticker import CexTicker
from datamaxi.datamaxi.cex_fee import CexFee
from datamaxi.datamaxi.cex_wallet_status import CexWalletStatus
from datamaxi.datamaxi.cex_announcement import CexAnnouncement
from datamaxi.datamaxi.cex_token import CexToken


class Cex(API):
    """Client to fetch CEX data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize CEX client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

        self.candle = CexCandle(api_key, **kwargs)
        self.ticker = CexTicker(api_key, **kwargs)
        self.fee = CexFee(api_key, **kwargs)
        self.wallet_status = CexWalletStatus(api_key, **kwargs)
        self.announcement = CexAnnouncement(api_key, **kwargs)
        self.token = CexToken(api_key, **kwargs)
