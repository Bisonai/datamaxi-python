from typing import Any, Dict, Optional
from datamaxi.api import API


class CexSymbol(API):
    """Client to fetch per-base / per-symbol CEX metadata + aggregates."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def metadata(
        self, exchange: Optional[str] = None, base: Optional[str] = None
    ) -> Dict[str, Any]:
        """Trading status + caution + tags + delisting metadata.

        `GET /api/v1/cex/symbol/metadata`
        """
        params: Dict[str, Any] = {}
        if exchange is not None:
            params["exchange"] = exchange
        if base is not None:
            params["base"] = base
        return self.query("/api/v1/cex/symbol/metadata", params)

    def tags(
        self, exchange: Optional[str] = None, base: Optional[str] = None
    ) -> Dict[str, Any]:
        """Exchange-assigned tags (e.g. seed, alpha) per symbol.

        `GET /api/v1/cex/symbol/tags`
        """
        params: Dict[str, Any] = {}
        if exchange is not None:
            params["exchange"] = exchange
        if base is not None:
            params["base"] = base
        return self.query("/api/v1/cex/symbol/tags", params)

    def cautions(
        self, exchange: Optional[str] = None, base: Optional[str] = None
    ) -> Dict[str, Any]:
        """Active caution / investment-warning flags per symbol.

        `GET /api/v1/cex/symbol/cautions`
        """
        params: Dict[str, Any] = {}
        if exchange is not None:
            params["exchange"] = exchange
        if base is not None:
            params["base"] = base
        return self.query("/api/v1/cex/symbol/cautions", params)

    def delistings(
        self, exchange: Optional[str] = None, base: Optional[str] = None
    ) -> Dict[str, Any]:
        """Scheduled delistings with timestamps.

        `GET /api/v1/cex/symbol/delistings`
        """
        params: Dict[str, Any] = {}
        if exchange is not None:
            params["exchange"] = exchange
        if base is not None:
            params["base"] = base
        return self.query("/api/v1/cex/symbol/delistings", params)

    def volume(self, base: str, exchange: Optional[str] = None) -> Dict[str, Any]:
        """Per-exchange 24h volume for a single base asset.

        `GET /api/v1/cex/symbol/volume`
        """
        params: Dict[str, Any] = {"base": base}
        if exchange is not None:
            params["exchange"] = exchange
        return self.query("/api/v1/cex/symbol/volume", params)

    def oi(self, base: str, exchange: Optional[str] = None) -> Dict[str, Any]:
        """Per-exchange Open Interest for a single base asset.

        `GET /api/v1/cex/symbol/oi`
        """
        params: Dict[str, Any] = {"base": base}
        if exchange is not None:
            params["exchange"] = exchange
        return self.query("/api/v1/cex/symbol/oi", params)

    def oi_stats(
        self,
        base: str,
        exchange: Optional[str] = None,
        currency: str = "USD",
    ) -> Dict[str, Any]:
        """Per-exchange OI snapshot with 1h / 4h / 24h deltas.

        `GET /api/v1/cex/symbol/oi-stats`

        Args:
            base (str): Base asset (e.g. ``BTC``).
            exchange (str): Optional single-exchange filter.
            currency (str): ``USD`` or ``KRW``.
        """
        if currency not in ("USD", "KRW"):
            raise ValueError("currency must be either USD or KRW")
        params: Dict[str, Any] = {"base": base, "currency": currency}
        if exchange is not None:
            params["exchange"] = exchange
        return self.query("/api/v1/cex/symbol/oi-stats", params)

    def liquidation(self, base: str, window: str = "24h") -> Dict[str, Any]:
        """Per-exchange long / short liquidation aggregates over a window.

        `GET /api/v1/cex/symbol/liquidation`

        Args:
            base (str): Base asset (e.g. ``BTC``).
            window (str): Time window (``1h``, ``24h``, ``7d`` — server caps at 30d).
        """
        return self.query(
            "/api/v1/cex/symbol/liquidation", {"base": base, "window": window}
        )
