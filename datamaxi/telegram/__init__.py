from typing import Any, Dict, Optional
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

    def channels(
        self,
        category: Optional[str] = None,
        page: int = 1,
        limit: int = 1000,
        sort: str = "desc",
    ) -> Dict[str, Any]:
        """Get Telegram supported channels

        `GET /api/v1/telegram/channels`

        <https://docs.datamaxi.finance/api/datasets/trend/telegram/channels>

        Args:
            category (str): channel category
            page (int): Page number
            limit (int): Limit of data
            sort (str): Sort order

        Returns:
            List of supported Telegram channels
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "category": category,
            "page": page,
            "limit": limit,
            "sort": sort,
        }

        res = self.query("/api/v1/telegram/channels", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                category=category,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request

    def posts(
        self,
        channel_username: Optional[str] = None,
        page: int = 1,
        limit: int = 1000,
        sort: str = "desc",
    ) -> Dict[str, Any]:
        """Get Telegram posts for given channel username

        `GET /api/v1/telegram/posts`

        <https://docs.datamaxiplus.com/api/datasets/trend/telegram/posts>

        Args:
            channel_username (str): channel username to search posts for
            page (int): Page number
            limit (int): Limit of data
            sort (str): Sort order

        Returns:
            Telegram post data in list of dictionary
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "channel": channel_username,
            "page": page,
            "limit": limit,
            "sort": sort,
        }

        res = self.query("/api/v1/telegram/posts", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                channel_username=channel_username,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request
