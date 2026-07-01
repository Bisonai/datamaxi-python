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
        self,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        market: Optional[str] = None,
        quote: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Trading status + caution + tags + delisting metadata.

        `GET /api/v1/cex/symbol/metadata`

        Args:
            exchange (str): Comma-separated exchange names (empty = all).
            base (str): Base asset filter.
            market (str): ``spot`` or ``futures`` (empty = both).
            quote (str): Quote asset filter.
            status (str): ``trading_status`` filter (comma-separated).
        """
        return self.request_endpoint(
            "cex_symbol_metadata",
            exchange=exchange,
            base=base,
            market=market,
            quote=quote,
            status=status,
        )

    def tags(
        self,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        tag: Optional[str] = None,
        market: Optional[str] = None,
        source: Optional[str] = None,
        min_confidence: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Exchange-assigned tags (e.g. seed, alpha) per symbol.

        `GET /api/v1/cex/symbol/tags`

        Args:
            exchange (str): Exchange filter (comma-separated).
            base (str): Base asset filter.
            tag (str): Tag filter (comma-separated).
            market (str): ``spot`` or ``futures``.
            source (str): Tag source filter
                (``rest_native``, ``announcement``, ``cmc``, ``manual``).
            min_confidence (int): Minimum confidence (0-100).
        """
        return self.request_endpoint(
            "cex_symbol_tags",
            exchange=exchange,
            base=base,
            tag=tag,
            market=market,
            source=source,
            min_confidence=min_confidence,
        )

    def cautions(
        self,
        exchange: Optional[str] = None,
        market: Optional[str] = None,
        min_level: Optional[str] = None,
        active_only: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Active caution / investment-warning flags per symbol.

        `GET /api/v1/cex/symbol/cautions`

        Args:
            exchange (str): Exchange filter (comma-separated, empty = all).
            market (str): ``spot`` or ``futures``.
            min_level (str): Minimum severity
                (``caution``, ``warning``, ``danger``).
            active_only (bool): Exclude rows whose ``end_at`` is in the past.
        """
        return self.request_endpoint(
            "cex_symbol_cautions",
            exchange=exchange,
            market=market,
            min_level=min_level,
            active_only=active_only,
        )

    def delistings(
        self,
        exchange: Optional[str] = None,
        market: Optional[str] = None,
        from_ms: Optional[int] = None,
        to_ms: Optional[int] = None,
        include_past: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Scheduled delistings with timestamps.

        `GET /api/v1/cex/symbol/delistings`

        Args:
            exchange (str): Exchange filter (comma-separated).
            market (str): ``spot`` or ``futures``.
            from_ms (int): Lower bound for ``delisting_at`` (ms epoch).
            to_ms (int): Upper bound for ``delisting_at`` (ms epoch).
            include_past (bool): Include already-delisted rows.
        """
        return self.request_endpoint(
            "cex_symbol_delistings",
            exchange=exchange,
            market=market,
            from_ms=from_ms,
            to_ms=to_ms,
            include_past=include_past,
        )

    def volume(self, base: str, market: Optional[str] = None) -> Dict[str, Any]:
        """Per-exchange 24h volume for a single base asset.

        `GET /api/v1/cex/symbol/volume`

        Args:
            base (str): Base asset (e.g. ``BTC``).
            market (str): Filter to ``spot`` or ``futures``.
        """
        return self.request_endpoint("cex_symbol_volume", base=base, market=market)

    def oi(self, base: str, exchange: Optional[str] = None) -> Dict[str, Any]:
        """Per-exchange Open Interest for a single base asset.

        `GET /api/v1/cex/symbol/oi`
        """
        return self.request_endpoint("cex_symbol_oi", base=base, exchange=exchange)

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
        return self.request_endpoint(
            "cex_symbol_oi_stats",
            base=base,
            exchange=exchange,
            currency=currency,
        )

    def liquidation(self, base: str, window: str = "24h") -> Dict[str, Any]:
        """Per-exchange long / short liquidation aggregates over a window.

        `GET /api/v1/cex/symbol/liquidation`

        Args:
            base (str): Base asset (e.g. ``BTC``).
            window (str): Time window (``1h``, ``24h``, ``7d`` — server caps at 30d).
        """
        return self.request_endpoint("cex_symbol_liquidation", base=base, window=window)
