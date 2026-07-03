from typing import Any, Dict
from datamaxi.api import Resource
from datamaxi.lib.utils import check_required_parameter


class MarginBorrow(Resource):
    """Client to fetch margin borrow data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize margin borrow client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

        self.__module__ = __name__
        self.__qualname__ = self.__class__.__qualname__

    def __call__(self, asset: str) -> Dict[str, Any]:
        """Fetch margin borrow data for a single asset.

        `GET /api/v1/margin-borrow`

        Args:
            asset (str): Token base asset (e.g. ``BTC``).

        Returns:
            Margin borrow response.
        """
        check_required_parameter(asset, "asset")
        return self.request_endpoint("margin_borrow", asset=asset)
