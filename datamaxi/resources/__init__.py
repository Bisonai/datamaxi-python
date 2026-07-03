from typing import Any
from datamaxi.api import API
from datamaxi.lib.constants import BASE_URL
from datamaxi.resources.cex import Cex
from datamaxi.resources.funding_rate import FundingRate
from datamaxi.resources.forex import Forex
from datamaxi.resources.premium import Premium
from datamaxi.resources.liquidation import Liquidation
from datamaxi.resources.open_interest import OpenInterest
from datamaxi.resources.margin_borrow import MarginBorrow
from datamaxi.resources.index_price import IndexPrice
from datamaxi.resources.cex_candle import CexCandle  # used in documentation # noqa:F401
from datamaxi.resources.cex_ticker import (  # used in documentation # noqa:F401
    CexTicker,
)
from datamaxi.resources.cex_fee import (  # used in documentation # noqa:F401
    CexFee,
)
from datamaxi.resources.cex_wallet_status import (  # used in documentation # noqa:F401
    CexWalletStatus,
)
from datamaxi.resources.cex_announcement import (  # used in documentation # noqa:F401
    CexAnnouncement,
)
from datamaxi.resources.cex_token import (  # used in documentation # noqa:F401
    CexToken,
)
from datamaxi.resources.cex_symbol import (  # used in documentation # noqa:F401
    CexSymbol,
)


class Datamaxi:
    """Client to fetch unified data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL

        # One shared transport — a single `requests.Session` / connection
        # pool threaded through every sub-client instead of each opening
        # its own. Sub-clients receive it via `api=` and forward it down.
        api = API(api_key, **kwargs)

        self.cex = Cex(api=api)
        self.funding_rate = FundingRate(api=api)
        self.forex = Forex(api=api)
        self.premium = Premium(api=api)
        # Futures-only surfaces. Top-level on the client so callers
        # reach them via `client.liquidation.heatmap(...)` /
        # `client.open_interest.summary(...)` — matches the
        # `/api/v1/{liquidation,open-interest}/*` REST grouping and
        # mirrors the equivalent typed wrappers in the Rust SDK
        # (`datamaxi::generated::{Liquidation, OpenInterest}`).
        self.liquidation = Liquidation(api=api)
        self.open_interest = OpenInterest(api=api)
        self.margin_borrow = MarginBorrow(api=api)
        self.index_price = IndexPrice(api=api)
