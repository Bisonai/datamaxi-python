from typing import Any, Dict, Optional
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.constants import Interval


class IndexPrice(API):
    """Client to fetch historical index price data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize index price client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

        self.__module__ = __name__
        self.__qualname__ = self.__class__.__qualname__

    def __call__(
        self,
        asset: str,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        interval: Interval = "5m",
    ) -> Dict[str, Any]:
        """Fetch historical index price data for a single asset.

        `GET /api/v1/index-price`

        Args:
            asset (str): Asset (e.g. ``BTC``).
            from_ (str): Start time. Defaults to ``now - 1 month``.
            to (str): End time. Defaults to ``now``.
            interval (str): Sampling interval (default ``5m``).

        Note:
            ``from_`` is named with a trailing underscore because ``from``
            is a Python keyword. The wire-level query param remains ``from``.

        Returns:
            Historical index price response.
        """
        check_required_parameter(asset, "asset")
        return self.request_endpoint(
            "index_price",
            asset=asset,
            interval=interval,
            **{"from": from_, "to": to},
        )
