from typing import Any, Dict, Optional, Tuple, Callable
from datamaxi.api import API
from datamaxi.lib.constants import ASC, DESC


class CexAnnouncement(API):
    """Client to fetch announcement data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def __call__(
        self,
        page: int = 1,
        limit: int = 1000,
        sort: str = DESC,
        key: Optional[str] = None,
        exchange: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Callable]:
        """Get exchange announcements

        `GET /api/v1/cex/announcements`

        <https://docs.datamaxiplus.com/rest/cex/announcements>

        Args:
            page (int): Page number
            limit (int): Limit of data
            sort (str): Sort order
            key (str): Key to sort by
            exchange (str): Exchange name filter
            category (str): Announcement category

        Returns:
            Tuple of announcement response and next request function
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "page": page,
            "limit": limit,
            "sort": sort,
            "key": key,
            "exchange": exchange,
            "category": category,
        }

        res = self.query("/api/v1/cex/announcements", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.__call__(
                key=key,
                exchange=exchange,
                category=category,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request
