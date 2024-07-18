from typing import Any, Callable, Tuple, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.constants import BASE_URL
from datamaxi.datamaxi.candle import Candle
from datamaxi.datamaxi.funding_rate import FundingRate


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

        self.candle = Candle(api_key, **kwargs)
        self.funding_rate = FundingRate(api_key, **kwargs)
