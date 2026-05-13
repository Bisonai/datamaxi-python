from typing import Any, Dict, Optional
from datamaxi.api import API


class Liquidation(API):
    """Client to fetch CEX futures liquidation data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def __call__(
        self,
        exchange: str,
        symbol: str,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """Recent liquidation events for a specific futures symbol.

        `GET /api/v1/liquidation`

        Args:
            exchange (str): Exchange name (e.g. ``binance``).
            symbol (str): Exchange-native API symbol (e.g. ``BTC-USDT``).
            limit (int): Max events to return (server caps).

        Returns:
            Liquidation events response.
        """
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        params = {"exchange": exchange, "symbol": symbol, "limit": limit}
        return self.query("/api/v1/liquidation", params)

    def feed(self, limit: int = 100) -> Dict[str, Any]:
        """Firehose: most recent liquidation events across every symbol.

        `GET /api/v1/liquidation/feed`

        Args:
            limit (int): Max events to return.
        """
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        return self.query("/api/v1/liquidation/feed", {"limit": limit})

    def heatmap(
        self,
        window: str = "1h",
        topN: int = 10,
    ) -> Dict[str, Any]:
        """Token × exchange liquidation heatmap over a rolling window.

        `GET /api/v1/liquidation/heatmap`

        Args:
            window (str): Rolling window (``1h``, ``4h``, or ``24h``).
            topN (int): Top N tokens by total (1-30).
        """
        if topN < 1 or topN > 30:
            raise ValueError("topN must be between 1 and 30")
        return self.query(
            "/api/v1/liquidation/heatmap", {"window": window, "topN": topN}
        )

    def map(
        self,
        base: str,
        exchange: str = "binance",
        quote: str = "USDT",
    ) -> Dict[str, Any]:
        """Coinglass-style liquidation map (price × leverage tier).

        `GET /api/v1/liquidation/map`

        Args:
            base (str): Base asset (e.g. ``BTC``).
            exchange (str): Exchange (default ``binance``).
            quote (str): Quote asset (default ``USDT``).
        """
        params = {"base": base, "exchange": exchange, "quote": quote}
        return self.query("/api/v1/liquidation/map", params)

    def symbol_history(
        self,
        symbol: str,
        quote: str = "USDT",
        exchange: Optional[str] = None,
        interval: str = "5m",
        window: str = "24h",
    ) -> Dict[str, Any]:
        """Bucketed long / short liquidation USD time series + price line.

        `GET /api/v1/liquidation/symbol-history`

        Args:
            symbol (str): Base asset (e.g. ``BTC``).
            quote (str): Quote asset (default ``USDT``).
            exchange (str): Optional exchange filter for the liquidation
                aggregation. Price line stays on Binance unless set.
            interval (str): Bucket interval (``5m``, ``15m``, or ``1h``).
            window (str): Lookback window (``24h``, ``72h``, or ``7d``).
        """
        params = {
            "symbol": symbol,
            "quote": quote,
            "interval": interval,
            "window": window,
        }
        if exchange is not None:
            params["exchange"] = exchange
        return self.query("/api/v1/liquidation/symbol-history", params)
