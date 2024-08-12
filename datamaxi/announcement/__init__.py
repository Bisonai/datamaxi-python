from typing import Any, List, Optional
from datamaxi.api import API
from datamaxi.lib.constants import BASE_URL


class Announcement(API):
    """Client to fetch Announcement data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def notice(self, category: Optional[str] = None) -> List[str]:
        """Get Exchange Announcements

        `GET /api/v1/announcements`

        <https://docs.datamaxi.finance/api/datasets/announcements>

        Returns:
            List of exchange announcements
        """
        params = {}
        if category:
            params["category"] = category

        url_path = "/api/v1/announcements"
        return self.query(url_path, params)
