from typing import Any
from datamaxi.lib.constants import BASE_URL
from datamaxi.datamaxi.cex import Cex
from datamaxi.datamaxi.dex import Dex
from datamaxi.datamaxi.funding_rate import FundingRate
from datamaxi.datamaxi.forex import Forex
from datamaxi.datamaxi.premium import Premium
from datamaxi.datamaxi.cex_candle import CexCandle  # used in documentation # noqa:F401
from datamaxi.datamaxi.cex_ticker import (  # used in documentation # noqa:F401
    CexTicker,
)
from datamaxi.datamaxi.cex_fee import (  # used in documentation # noqa:F401
    CexFee,
)
from datamaxi.datamaxi.cex_wallet_status import (  # used in documentation # noqa:F401
    CexWalletStatus,
)
from datamaxi.datamaxi.cex_announcement import (  # used in documentation # noqa:F401
    CexAnnouncement,
)
from datamaxi.datamaxi.cex_token import (  # used in documentation # noqa:F401
    CexToken,
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

        self.cex = Cex(api_key, **kwargs)
        self.dex = Dex(api_key, **kwargs)
        self.funding_rate = FundingRate(api_key, **kwargs)
        self.forex = Forex(api_key, **kwargs)
        self.premium = Premium(api_key, **kwargs)
