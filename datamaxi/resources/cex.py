from typing import Any
from datamaxi.api import Resource
from datamaxi.resources.cex_candle import CexCandle
from datamaxi.resources.cex_ticker import CexTicker
from datamaxi.resources.cex_fee import CexFee
from datamaxi.resources.cex_wallet_status import CexWalletStatus
from datamaxi.resources.cex_announcement import CexAnnouncement
from datamaxi.resources.cex_token import CexToken
from datamaxi.resources.cex_symbol import CexSymbol


class Cex(Resource):
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
        # Per-base / per-symbol surfaces (metadata, tags, cautions,
        # delistings, volume, OI / OI-stats / liquidation aggregates).
        # Grouped under `cex.symbol` to mirror the REST path layout
        # (`/api/v1/cex/symbol/*`) and to keep the top-level `Cex`
        # surface flat.
        self.symbol = CexSymbol(api_key, **kwargs)
