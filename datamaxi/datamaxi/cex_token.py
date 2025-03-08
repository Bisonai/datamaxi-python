from typing import Any, Dict, Optional
from datamaxi.api import API
from datamaxi.lib.constants import DESC, ASC


class CexToken(API):
    """Client to fetch token update data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize token update client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def updates(
        self,
        type: Optional[str] = None,
        page: int = 1,
        limit: int = 1000,
        sort: str = DESC,
    ) -> Dict[str, Any]:
        """Get token update data

        `GET /api/v1/token/updates`

        <https://docs.datamaxiplus.com/rest/cex/token-updates>

        Args:
            type (str): Update type
            page (int): Page number
            limit (int): Limit of data
            sort (str): Sort order

        Returns:
            Token update data in list of dictionary
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        if type is not None and type not in ["listed", "delisted"]:
            raise ValueError("type must be either listed or delisted when set")

        params = {
            "type": type,
            "page": page,
            "limit": limit,
            "sort": sort,
        }

        res = self.query("/api/v1/cex/token/updates", params)
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                type=type,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request
