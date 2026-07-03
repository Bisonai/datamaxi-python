from typing import Any, Dict, Optional
from datamaxi.api import Resource
from datamaxi.lib.constants import Interval, SortOrder


class OpenInterest(Resource):
    """Client to fetch CEX futures Open Interest data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def __call__(self, exchange: str, symbol: str) -> Dict[str, Any]:
        """Latest Open Interest snapshot for a single futures symbol.

        `GET /api/v1/open-interest`

        Args:
            exchange (str): Exchange (e.g. ``binance``).
            symbol (str): Exchange-native API symbol (e.g. ``BTC-USDT``).
        """
        return self.request_endpoint("open_interest", exchange=exchange, symbol=symbol)

    def list(self, exchange: Optional[str] = None) -> Dict[str, Any]:
        """List all (exchange, symbol) pairs currently reporting OI.

        `GET /api/v1/open-interest/list`

        Args:
            exchange (str): Optional filter to one exchange.
        """
        return self.request_endpoint("open_interest_list", exchange=exchange)

    def overview(
        self,
        page: int = 1,
        limit: int = 20,
        key: str = "binance",
        sort: SortOrder = "desc",
        query: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Paginated token × exchange OI matrix.

        `GET /api/v1/open-interest/overview`

        Args:
            page (int): Page number.
            limit (int): Page size.
            key (str): Exchange to sort by.
            sort (str): Sort direction (``asc`` or ``desc``).
            query (str): Optional base-symbol search filter.
        """
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if sort not in ("asc", "desc"):
            raise ValueError("sort must be either asc or desc")
        return self.request_endpoint(
            "open_interest_overview",
            page=page,
            limit=limit,
            key=key,
            sort=sort,
            query=query,
        )

    def summary(self, topN: int = 10) -> Dict[str, Any]:
        """Top-line OI aggregates (total USD, top tokens, top exchanges).

        `GET /api/v1/open-interest/summary`

        Args:
            topN (int): Top N tokens to return (1-30).
        """
        if topN < 1 or topN > 30:
            raise ValueError("topN must be between 1 and 30")
        return self.request_endpoint("open_interest_summary", top_n=topN)

    def history_aggregated(
        self,
        token_id: str,
        interval: Interval = "1h",
        from_: Optional[int] = None,
        to: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Per-exchange aggregated OI history for a single token.

        `GET /api/v1/open-interest/history-aggregated`

        Args:
            token_id (str): Token id (e.g. ``bitcoin``).
            interval (str): Aggregation interval (``5m``, ``15m``, ``1h``,
                ``4h``, or ``1d``).
            from_ (int): Start unix-ms. Default depends on interval
                (7d for 1h, 30d for 4h, 1y for 1d).
            to (int): End unix-ms. Defaults to now.

        Note:
            ``from_`` is named with a trailing underscore because ``from``
            is a Python keyword. The wire-level query param remains ``from``.
        """
        return self.request_endpoint(
            "open_interest_history_aggregated",
            token_id=token_id,
            interval=interval,
            **{"from": from_, "to": to},
        )
