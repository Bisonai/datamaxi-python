from typing import Any, List, Union, Optional
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.constants import BASE_URL


class Telegram(API):
    """Client to fetch Telegram data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def channels(self, category: Optional[str] = None) -> List[str]:
        """Get Telegram supported channels

        `GET /api/v1/telegram/channels`

        <https://docs.datamaxi.finance/api/datasets/trend/telegram/channels>

        Returns:
            List of supported Telegram channels
        """
        params = {}
        if category:
            params["category"] = category

        url_path = "/api/v1/telegram/channels"
        return self.query(url_path, params)

    def posts(
        self, channel_username: Optional[str] = None
    ) -> Union[List, pd.DataFrame]:
        """Get Telegram posts for given channel username

        `GET /api/v1/telegram/posts`

        <https://docs.datamaxiplus.com/api/datasets/trend/telegram/posts>

        Args:
            channel_username (str): channel username to search posts for

        Returns:
            Telegram post data
        """
        params = {}
        if channel_username:
            params["channel"] = channel_username
        return self.query("/api/v1/telegram/posts", params)
