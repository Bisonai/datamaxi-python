from typing import Any, Optional, Tuple, Callable
from datamaxi.api import Resource
from datamaxi.resources.responses import TokenUpdateResponse


class CexToken(Resource):
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
        page: int = 1,
        limit: int = 1000,
        type: Optional[str] = None,
    ) -> Tuple[TokenUpdateResponse, Callable]:
        """Get token update data

        `GET /api/v1/cex/token/updates`

        <https://docs.datamaxiplus.com/rest/cex/token-updates>

        Args:
            page (int): Page number
            limit (int): Limit of data
            type (str): Update type

        Returns:
            Tuple of token update response and next request function
        """
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if type is not None and type not in ["listed", "delisted"]:
            raise ValueError("type must be either listed or delisted when set")

        res = self.request_endpoint(
            "cex_token_updates", page=page, limit=limit, type=type
        )
        if res["data"] is None:
            raise ValueError("no data found")

        def next_request():
            return self.updates(
                type=type,
                page=page + 1,
                limit=limit,
            )

        return res, next_request
