from typing import Any, Dict, Optional
from datamaxi.api import API
from datamaxi.lib.constants import BASE_URL


class Announcement(API):
    """Client to fetch announcement data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def get(
        self,
        category: Optional[str] = None,
        page: int = 1,
        limit: int = 1000,
        sort: str = "desc",
    ) -> Dict[str, Any]:
        """Get exchange announcements

        `GET /api/v1/announcements`

        <https://docs.datamaxiplus.com/api/datasets/announcements>

        Args:
            category (str): announcement category
            page (int): Page number
            limit (int): Limit of data
            sort (str): Sort order

        Returns:
            Announcements
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

        res = self.query("/api/v1/announcements", params)
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
