from typing import Any, List, Optional
from datamaxi.api import API
from datamaxi.lib.constants import BASE_URL


class Token(API):
    """Client to fetch Token status data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def updates(self, type: Optional[str] = None) -> List[str]:
        """Get Token Updates

        `GET /api/v1/token/updates`

        <https://docs.datamaxi.finance/api/datasets/token>

        Returns:
            List of token updates
        """
        params = {}
        if type:
            params["type"] = type

        url_path = "/api/v1/token/updates"
        return self.query(url_path, params)
