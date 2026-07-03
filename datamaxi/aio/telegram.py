"""Async Telegram client — mirror of ``datamaxi.telegram.Telegram``.

Standalone top-level async client (builds its own ``AsyncAPI``). Use as an
async context manager so the underlying httpx client is closed.
"""

from typing import Any, Optional, Tuple, Callable

from datamaxi.aio._core import AsyncAPI, AsyncResource
from datamaxi.resources.responses import (
    TelegramChannelsResponse,
    TelegramMessagesResponse,
)
from datamaxi.lib.constants import BASE_URL, SortOrder


class AsyncTelegram(AsyncResource):
    """Client to fetch Telegram data from DataMaxi+ API (async)."""

    def __init__(self, api_key=None, **kwargs: Any):
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(AsyncAPI(api_key, **kwargs))

    async def aclose(self):
        await self._api.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    def __repr__(self):
        return "AsyncTelegram(base_url={!r}, has_key={})".format(
            self._api.base_url, bool(self._api.api_key)
        )

    async def channels(
        self,
        page: int = 1,
        limit: int = 1000,
        category: Optional[str] = None,
        key: Optional[str] = None,
        sort: SortOrder = "desc",
    ) -> Tuple[TelegramChannelsResponse, Callable]:
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        res = await self.request_endpoint(
            "telegram_channels",
            page=page,
            limit=limit,
            category=category,
            key=key,
            sort=sort,
        )
        if res["data"] is None:
            raise ValueError("no data found")

        async def next_request():
            return await self.channels(
                category=category,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request

    async def messages(
        self,
        channel_name: Optional[str] = None,
        page: int = 1,
        limit: int = 1000,
        key: Optional[str] = None,
        sort: SortOrder = "desc",
        category: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> Tuple[TelegramMessagesResponse, Callable]:
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if sort not in ["asc", "desc"]:
            raise ValueError("sort must be either asc or desc")

        res = await self.request_endpoint(
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

        async def next_request():
            return await self.messages(
                channel_name=channel_name,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request
