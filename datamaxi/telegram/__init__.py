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
        page: int = 1,
        limit: int = 1000,
        category: Optional[str] = None,
        key: Optional[str] = None,
        sort: str = "desc",
    ) -> Dict[str, Any]:
        """Get Telegram supported channels

        `GET /api/v1/telegram/channels`

        <https://docs.datamaxiplus.com/rest/telegram/channels>

        Args:
            page (int): Page number
            limit (int): Limit of data
            category (str): channel category
            key (str): Specifies key to sort by
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
            "page": page,
            "limit": limit,
            "category": category,
            "key": key,
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

    def messages(
        self,
        channel_name: Optional[str] = None,
        page: int = 1,
        limit: int = 1000,
        key: Optional[str] = None,
        sort: str = "desc",
        category: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get Telegram posts for given channel username

        `GET /api/v1/telegram/messages`

        <https://docs.datamaxiplus.com/rest/telegram/messages>

        Args:
            channel_name (str): channel name to get posts from
            page (int): Page number
            limit (int): Limit of data
            key (str): Specifies key to sort by
            sort (str): Sort order
            category (str): Specifies category

        Returns:
            Telegram channel posts
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "channel": channel_name,
            "page": page,
            "limit": limit,
            "key": key,
            "sort": sort,
            "category": category,
        }

        res = self.query("/api/v1/telegram/messages", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                channel_name=channel_name,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request
