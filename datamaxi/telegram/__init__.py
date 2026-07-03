from typing import Any, Optional, Tuple, Callable
from datamaxi.api import Resource
from datamaxi.resources.responses import (
    TelegramChannelsResponse,
    TelegramMessagesResponse,
)
from datamaxi.lib.constants import BASE_URL, SortOrder


class Telegram(Resource):
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
        sort: SortOrder = "desc",
    ) -> Tuple[TelegramChannelsResponse, Callable]:
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
            Tuple of channel response and next request function
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        res = self.request_endpoint(
            "telegram_channels",
            page=page,
            limit=limit,
            category=category,
            key=key,
            sort=sort,
        )
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.channels(
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
        sort: SortOrder = "desc",
        category: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> Tuple[TelegramMessagesResponse, Callable]:
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
            search_query (str): Specifies search query

        Returns:
            Tuple of message response and next request function
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        res = self.request_endpoint(
            "telegram_messages",
            channel=channel_name,
            page=page,
            limit=limit,
            key=key,
            sort=sort,
            category=category,
            search_query=search_query,
        )
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.messages(
                channel_name=channel_name,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request
