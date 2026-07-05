"""
Auto-generated typed response models from openapi.yaml.
DO NOT EDIT — regenerate with: make python

Hint-only dataclasses describing the typed JSON returned by the data endpoints.
Attribute names use the friendly / snake_case form; ``from_dict`` maps the raw
wire keys onto them and tolerates missing fields (a drifted or partial payload
yields zero-valued attributes rather than raising) — the Python analogue of the
generated Rust structs' ``#[serde(default)]``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional  # noqa: F401


def _as_model(model, value):
    """Build a nested response model, tolerating a missing/non-object value."""
    return model.from_dict(value) if isinstance(value, dict) else None


def _as_models(model, value):
    """Build a list of nested response models, tolerating missing items."""
    return [model.from_dict(x) for x in value or [] if isinstance(x, dict)]


@dataclass
class CexAnnouncementsResponse:
    # specifies the exchanges of the announcements
    category: List[str] = field(default_factory=list)
    # `Data` specifies an array of the announcements
    data: List[CexAnnouncementsView] = field(default_factory=list)
    # specifies the categories of the announcements
    exchange: List[str] = field(default_factory=list)
    key: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    total: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> CexAnnouncementsResponse:
        return cls(
            category=data.get("category") or [],
            data=_as_models(CexAnnouncementsView, data.get("data")),
            exchange=data.get("exchange") or [],
            key=data.get("key", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            total=data.get("total", 0),
        )


@dataclass
class CexAnnouncementsView:
    # specifies the category of the announcement
    c: str = ""
    # specifies the date of the announcement
    d: int = 0
    # specifies the exchange of the announcement
    e: str = ""
    # specifies the summary of the announcement
    s: str = ""
    # specifies the title of the announcement
    t: str = ""
    # specifies the URL of the announcement
    u: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> CexAnnouncementsView:
        return cls(
            c=data.get("c", ""),
            d=data.get("d", 0),
            e=data.get("e", ""),
            s=data.get("s", ""),
            t=data.get("t", ""),
            u=data.get("u", ""),
        )


@dataclass
class CexCandleResponse:
    currency: str = ""
    data: List[CexCandleView] = field(default_factory=list)
    exchange: str = ""
    interval: str = ""
    market: str = ""
    symbol: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> CexCandleResponse:
        return cls(
            currency=data.get("currency", ""),
            data=_as_models(CexCandleView, data.get("data")),
            exchange=data.get("exchange", ""),
            interval=data.get("interval", ""),
            market=data.get("market", ""),
            symbol=data.get("symbol", ""),
        )


@dataclass
class CexCandleView:
    # specifies close price of the candle
    c: float = 0.0
    # specifies the opening date and time of candle
    d: int = 0
    # specifies high price of the candle
    h: float = 0.0
    # specifies low price of the candle
    l: float = 0.0
    # specifies open price of the candle
    o: float = 0.0
    # specifies trading volume (base token) of the candle
    v: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> CexCandleView:
        return cls(
            c=data.get("c", 0.0),
            d=data.get("d", 0),
            h=data.get("h", 0.0),
            l=data.get("l", 0.0),
            o=data.get("o", 0.0),
            v=data.get("v", 0.0),
        )


@dataclass
class CexTokenUpdatesResponse:
    # `data` specifies an array of the token updates
    data: List[CexTokenUpdatesView] = field(default_factory=list)
    key: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    total: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> CexTokenUpdatesResponse:
        return cls(
            data=_as_models(CexTokenUpdatesView, data.get("data")),
            key=data.get("key", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            total=data.get("total", 0),
        )


@dataclass
class CexTokenUpdatesView:
    # Specifies the base token
    b: str = ""
    # Specifies the timestamp
    d: int = 0
    # Specifies the exchange
    e: str = ""
    # Specifies the market
    m: str = ""
    # Specifies the quote token
    q: str = ""
    # Specifies the type of the token update (listed or delisted)
    t: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> CexTokenUpdatesView:
        return cls(
            b=data.get("b", ""),
            d=data.get("d", 0),
            e=data.get("e", ""),
            m=data.get("m", ""),
            q=data.get("q", ""),
            t=data.get("t", ""),
        )


@dataclass
class ForexResponse:
    # specifies the unix timestamp of the forex rate
    d: int = 0
    # specifies the forex rate
    r: float = 0.0
    # specifies the name of the forex symbol
    s: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> ForexResponse:
        return cls(
            d=data.get("d", 0),
            r=data.get("r", 0.0),
            s=data.get("s", ""),
        )


@dataclass
class FundingRateHistoryResponse:
    data: List[FundingRateHistoryView] = field(default_factory=list)
    exchange: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    symbol: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> FundingRateHistoryResponse:
        return cls(
            data=_as_models(FundingRateHistoryView, data.get("data")),
            exchange=data.get("exchange", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            symbol=data.get("symbol", ""),
        )


@dataclass
class FundingRateHistoryView:
    # specifies the date and time in UNIX timestamp format
    d: int = 0
    # specifies the funding rate
    f: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> FundingRateHistoryView:
        return cls(
            d=data.get("d", 0),
            f=data.get("f", 0.0),
        )


@dataclass
class FundingRateLatestResponse:
    # Specifies the base
    b: str = ""
    # Specifies the timestamp
    d: int = 0
    # Specifies the exchange
    e: str = ""
    # Specifies the funding rate
    f: float = 0.0
    # Specifies the interval hours
    i: int = 0
    # Specifies the token id
    id: str = ""
    # Specifies the processed at
    p: int = 0
    # Specifies the quote
    q: str = ""
    # Specifies the symbol
    s: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> FundingRateLatestResponse:
        return cls(
            b=data.get("b", ""),
            d=data.get("d", 0),
            e=data.get("e", ""),
            f=data.get("f", 0.0),
            i=data.get("i", 0),
            id=data.get("id", ""),
            p=data.get("p", 0),
            q=data.get("q", ""),
            s=data.get("s", ""),
        )


@dataclass
class IndexPriceResponse:
    data: List[IndexPriceView] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> IndexPriceResponse:
        return cls(
            data=_as_models(IndexPriceView, data.get("data")),
        )


@dataclass
class IndexPriceView:
    price: float = 0.0
    timestamp: int = 0
    volume: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> IndexPriceView:
        return cls(
            price=data.get("price", 0.0),
            timestamp=data.get("timestamp", 0),
            volume=data.get("volume", 0.0),
        )


@dataclass
class LiquidationEntry:
    base: str = ""
    exchange: str = ""
    price: float = 0.0
    price_usd: float = 0.0
    quote: str = ""
    side: str = ""
    symbol: str = ""
    timestamp: int = 0
    token_id: str = ""
    volume: float = 0.0
    volume_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationEntry:
        return cls(
            base=data.get("base", ""),
            exchange=data.get("exchange", ""),
            price=data.get("price", 0.0),
            price_usd=data.get("priceUsd", 0.0),
            quote=data.get("quote", ""),
            side=data.get("side", ""),
            symbol=data.get("symbol", ""),
            timestamp=data.get("timestamp", 0),
            token_id=data.get("tokenId", ""),
            volume=data.get("volume", 0.0),
            volume_usd=data.get("volumeUsd", 0.0),
        )


@dataclass
class LiquidationFeedEntry:
    base: str = ""
    exchange: str = ""
    price: float = 0.0
    price_usd: float = 0.0
    quote: str = ""
    side: str = ""
    symbol: str = ""
    timestamp: int = 0
    token_id: str = ""
    volume: float = 0.0
    volume_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationFeedEntry:
        return cls(
            base=data.get("base", ""),
            exchange=data.get("exchange", ""),
            price=data.get("price", 0.0),
            price_usd=data.get("priceUsd", 0.0),
            quote=data.get("quote", ""),
            side=data.get("side", ""),
            symbol=data.get("symbol", ""),
            timestamp=data.get("timestamp", 0),
            token_id=data.get("tokenId", ""),
            volume=data.get("volume", 0.0),
            volume_usd=data.get("volumeUsd", 0.0),
        )


@dataclass
class LiquidationFeedResponse:
    data: List[LiquidationFeedEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationFeedResponse:
        return cls(
            data=_as_models(LiquidationFeedEntry, data.get("data")),
        )


@dataclass
class LiquidationHeatmapCell:
    base: str = ""
    exchange: str = ""
    long_usd: float = 0.0
    short_usd: float = 0.0
    token_id: str = ""
    total_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationHeatmapCell:
        return cls(
            base=data.get("base", ""),
            exchange=data.get("exchange", ""),
            long_usd=data.get("longUsd", 0.0),
            short_usd=data.get("shortUsd", 0.0),
            token_id=data.get("tokenId", ""),
            total_usd=data.get("totalUsd", 0.0),
        )


@dataclass
class LiquidationHeatmapExchangesummary:
    exchange: str = ""
    long_usd: float = 0.0
    short_usd: float = 0.0
    total_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationHeatmapExchangesummary:
        return cls(
            exchange=data.get("exchange", ""),
            long_usd=data.get("longUsd", 0.0),
            short_usd=data.get("shortUsd", 0.0),
            total_usd=data.get("totalUsd", 0.0),
        )


@dataclass
class LiquidationHeatmapResponse:
    # (top tokens) × (all exchanges with data)
    cells: List[LiquidationHeatmapCell] = field(default_factory=list)
    # sorted desc, includes only venues with data
    exchanges: List[LiquidationHeatmapExchangesummary] = field(default_factory=list)
    # ms
    generated_at: int = 0
    grand_total: float = 0.0
    # top N by TotalUsd desc
    tokens: List[LiquidationHeatmapTokensummary] = field(default_factory=list)
    # "1h" | "4h" | "24h"
    window: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationHeatmapResponse:
        return cls(
            cells=_as_models(LiquidationHeatmapCell, data.get("cells")),
            exchanges=_as_models(
                LiquidationHeatmapExchangesummary, data.get("exchanges")
            ),
            generated_at=data.get("generatedAt", 0),
            grand_total=data.get("grandTotal", 0.0),
            tokens=_as_models(LiquidationHeatmapTokensummary, data.get("tokens")),
            window=data.get("window", ""),
        )


@dataclass
class LiquidationHeatmapTokensummary:
    base: str = ""
    long_usd: float = 0.0
    name: str = ""
    short_usd: float = 0.0
    symbol: str = ""
    token_id: str = ""
    total_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationHeatmapTokensummary:
        return cls(
            base=data.get("base", ""),
            long_usd=data.get("longUsd", 0.0),
            name=data.get("name", ""),
            short_usd=data.get("shortUsd", 0.0),
            symbol=data.get("symbol", ""),
            token_id=data.get("tokenId", ""),
            total_usd=data.get("totalUsd", 0.0),
        )


@dataclass
class LiquidationMapAssumptions:
    entry_samples: int = 0
    entry_window: str = ""
    long_share_of_oi: float = 0.0
    mmr: float = 0.0
    tiers: List[LiquidationMapTierassumption] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationMapAssumptions:
        return cls(
            entry_samples=data.get("entrySamples", 0),
            entry_window=data.get("entryWindow", ""),
            long_share_of_oi=data.get("longShareOfOi", 0.0),
            mmr=data.get("mmr", 0.0),
            tiers=_as_models(LiquidationMapTierassumption, data.get("tiers")),
        )


@dataclass
class LiquidationMapBucket:
    l100x_usd: float = 0.0
    l10x_usd: float = 0.0
    l25x_usd: float = 0.0
    l50x_usd: float = 0.0
    price: float = 0.0
    side: str = ""
    total_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationMapBucket:
        return cls(
            l100x_usd=data.get("l100xUsd", 0.0),
            l10x_usd=data.get("l10xUsd", 0.0),
            l25x_usd=data.get("l25xUsd", 0.0),
            l50x_usd=data.get("l50xUsd", 0.0),
            price=data.get("price", 0.0),
            side=data.get("side", ""),
            total_usd=data.get("totalUsd", 0.0),
        )


@dataclass
class LiquidationMapResponse:
    assumptions: Optional[LiquidationMapAssumptions] = None
    base: str = ""
    buckets: List[LiquidationMapBucket] = field(default_factory=list)
    # Cumulative totals — separately surfaced so the FE doesn't have to re-sum to drive the cumulative line series (Coinglass-style).
    cumulative_long_usd: float = 0.0
    cumulative_short_usd: float = 0.0
    current_price: float = 0.0
    exchange: str = ""
    generated_at: int = 0
    quote: str = ""
    symbol: str = ""
    total_oi_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationMapResponse:
        return cls(
            assumptions=_as_model(LiquidationMapAssumptions, data.get("assumptions")),
            base=data.get("base", ""),
            buckets=_as_models(LiquidationMapBucket, data.get("buckets")),
            cumulative_long_usd=data.get("cumulativeLongUsd", 0.0),
            cumulative_short_usd=data.get("cumulativeShortUsd", 0.0),
            current_price=data.get("currentPrice", 0.0),
            exchange=data.get("exchange", ""),
            generated_at=data.get("generatedAt", 0),
            quote=data.get("quote", ""),
            symbol=data.get("symbol", ""),
            total_oi_usd=data.get("totalOiUsd", 0.0),
        )


@dataclass
class LiquidationMapTierassumption:
    leverage: int = 0
    share: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationMapTierassumption:
        return cls(
            leverage=data.get("leverage", 0),
            share=data.get("share", 0.0),
        )


@dataclass
class LiquidationResponse:
    data: List[LiquidationEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationResponse:
        return cls(
            data=_as_models(LiquidationEntry, data.get("data")),
        )


@dataclass
class LiquidationStatsBiggest:
    base: str = ""
    exchange: str = ""
    quote: str = ""
    volume_usd: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationStatsBiggest:
        return cls(
            base=data.get("base", ""),
            exchange=data.get("exchange", ""),
            quote=data.get("quote", ""),
            volume_usd=data.get("volumeUsd", 0.0),
        )


@dataclass
class LiquidationStatsResponse:
    biggest: Optional[LiquidationStatsBiggest] = None
    # number of events
    count: int = 0
    # ms
    generated_at: int = 0
    # round(long/total*100), 0 when empty
    long_ratio: int = 0
    # sell-side
    long_usd: float = 0.0
    # buy-side
    short_usd: float = 0.0
    # long + short
    total: float = 0.0
    # distinct exchanges
    venues: int = 0
    # "1h" | "4h" | "24h"
    window: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationStatsResponse:
        return cls(
            biggest=_as_model(LiquidationStatsBiggest, data.get("biggest")),
            count=data.get("count", 0),
            generated_at=data.get("generatedAt", 0),
            long_ratio=data.get("longRatio", 0),
            long_usd=data.get("longUsd", 0.0),
            short_usd=data.get("shortUsd", 0.0),
            total=data.get("total", 0.0),
            venues=data.get("venues", 0),
            window=data.get("window", ""),
        )


@dataclass
class LiquidationSymbolHistoryBucket:
    # Liquidated long positions in USD over this bucket (Side='sell').
    long_usd: float = 0.0
    # Candle close mid for the same bucket. nil when no candle exists (very early in a newly listed pair, or when the price feed is down). FE renders the price line with `connectNulls=false` so gaps stay visible instead of being smoothed across.
    price: float = 0.0
    # Liquidated short positions in USD over this bucket (Side='buy').
    short_usd: float = 0.0
    # Convenience sum so the FE can drive a "total" line without re-add.
    total_usd: float = 0.0
    # Unix ms timestamp at the start of the interval bucket.
    ts: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationSymbolHistoryBucket:
        return cls(
            long_usd=data.get("longUsd", 0.0),
            price=data.get("price", 0.0),
            short_usd=data.get("shortUsd", 0.0),
            total_usd=data.get("totalUsd", 0.0),
            ts=data.get("ts", 0),
        )


@dataclass
class LiquidationSymbolHistoryResponse:
    buckets: List[LiquidationSymbolHistoryBucket] = field(default_factory=list)
    exchange: str = ""
    generated_at: int = 0
    interval: str = ""
    quote: str = ""
    symbol: str = ""
    # Totals over the window — handy for a header line without making the FE re-aggregate the bucket list.
    total_long_usd: float = 0.0
    total_short_usd: float = 0.0
    window: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> LiquidationSymbolHistoryResponse:
        return cls(
            buckets=_as_models(LiquidationSymbolHistoryBucket, data.get("buckets")),
            exchange=data.get("exchange", ""),
            generated_at=data.get("generatedAt", 0),
            interval=data.get("interval", ""),
            quote=data.get("quote", ""),
            symbol=data.get("symbol", ""),
            total_long_usd=data.get("totalLongUsd", 0.0),
            total_short_usd=data.get("totalShortUsd", 0.0),
            window=data.get("window", ""),
        )


@dataclass
class ListingsHistoricalResponse:
    data: List[ListingsHistoricalView] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> ListingsHistoricalResponse:
        return cls(
            data=_as_models(ListingsHistoricalView, data.get("data")),
        )


@dataclass
class ListingsHistoricalView:
    announced_at: int = 0
    base: str = ""
    deposit_at: int = 0
    exchange: str = ""
    network: Optional[str] = None
    trade_at: int = 0
    url: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> ListingsHistoricalView:
        return cls(
            announced_at=data.get("announced_at", 0),
            base=data.get("base", ""),
            deposit_at=data.get("deposit_at", 0),
            exchange=data.get("exchange", ""),
            network=data.get("network"),
            trade_at=data.get("trade_at", 0),
            url=data.get("url", ""),
        )


@dataclass
class MarginBorrowResponse:
    cross: Any = None
    isolated: Any = None

    @classmethod
    def from_dict(cls, data: dict) -> MarginBorrowResponse:
        return cls(
            cross=data.get("cross"),
            isolated=data.get("isolated"),
        )


@dataclass
class OpenInterestHistoryAggregatedResponse:
    # Data is keyed by exchange id → time-series points ordered by t asc.
    data: Any = None
    exchange_url: Any = None
    token: Optional[TokenDetail] = None

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestHistoryAggregatedResponse:
        return cls(
            data=data.get("data"),
            exchange_url=data.get("exchange_url"),
            token=_as_model(TokenDetail, data.get("token")),
        )


@dataclass
class OpenInterestListEntry:
    base: str = ""
    exchange: str = ""
    open_interest: float = 0.0
    open_interest_usd: float = 0.0
    quote: str = ""
    symbol: str = ""
    timestamp: int = 0
    token_id: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestListEntry:
        return cls(
            base=data.get("base", ""),
            exchange=data.get("exchange", ""),
            open_interest=data.get("openInterest", 0.0),
            open_interest_usd=data.get("openInterestUsd", 0.0),
            quote=data.get("quote", ""),
            symbol=data.get("symbol", ""),
            timestamp=data.get("timestamp", 0),
            token_id=data.get("tokenId", ""),
        )


@dataclass
class OpenInterestListResponse:
    data: List[OpenInterestListEntry] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestListResponse:
        return cls(
            data=_as_models(OpenInterestListEntry, data.get("data")),
        )


@dataclass
class OpenInterestOverviewResponse:
    data: List[OpenInterestOverviewView] = field(default_factory=list)
    key: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    total: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestOverviewResponse:
        return cls(
            data=_as_models(OpenInterestOverviewView, data.get("data")),
            key=data.get("key", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            total=data.get("total", 0),
        )


@dataclass
class OpenInterestOverviewView:
    exchanges: Any = None
    id: str = ""
    token: Optional[TokenDetail] = None

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestOverviewView:
        return cls(
            exchanges=data.get("exchanges"),
            id=data.get("id", ""),
            token=_as_model(TokenDetail, data.get("token")),
        )


@dataclass
class OpenInterestResponse:
    base: str = ""
    exchange: str = ""
    open_interest: float = 0.0
    open_interest_usd: float = 0.0
    quote: str = ""
    symbol: str = ""
    timestamp: int = 0
    token_id: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestResponse:
        return cls(
            base=data.get("base", ""),
            exchange=data.get("exchange", ""),
            open_interest=data.get("openInterest", 0.0),
            open_interest_usd=data.get("openInterestUsd", 0.0),
            quote=data.get("quote", ""),
            symbol=data.get("symbol", ""),
            timestamp=data.get("timestamp", 0),
            token_id=data.get("tokenId", ""),
        )


@dataclass
class OpenInterestSummaryExchangesummary:
    exchange: str = ""
    open_interest_usd: float = 0.0
    # Number of tokens this exchange has non-zero OI for.
    tokens: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestSummaryExchangesummary:
        return cls(
            exchange=data.get("exchange", ""),
            open_interest_usd=data.get("openInterestUsd", 0.0),
            tokens=data.get("tokens", 0),
        )


@dataclass
class OpenInterestSummaryResponse:
    # sorted desc, all venues with data
    exchanges: List[OpenInterestSummaryExchangesummary] = field(default_factory=list)
    generated_at: int = 0
    grand_total: float = 0.0
    # top N by OI desc
    tokens: List[OpenInterestSummaryTokensummary] = field(default_factory=list)
    # Token universe size — useful in the FE to label the KPI as "BTC of 1,234 tokens" instead of just "BTC".
    total_tokens: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestSummaryResponse:
        return cls(
            exchanges=_as_models(
                OpenInterestSummaryExchangesummary, data.get("exchanges")
            ),
            generated_at=data.get("generatedAt", 0),
            grand_total=data.get("grandTotal", 0.0),
            tokens=_as_models(OpenInterestSummaryTokensummary, data.get("tokens")),
            total_tokens=data.get("totalTokens", 0),
        )


@dataclass
class OpenInterestSummaryTokensummary:
    base: str = ""
    icon: str = ""
    name: str = ""
    open_interest_usd: float = 0.0
    symbol: str = ""
    token_id: str = ""
    # Number of exchanges this token is listed on with non-zero OI. Useful for the breakdown card to show e.g. "BTC · 8 venues".
    venues: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> OpenInterestSummaryTokensummary:
        return cls(
            base=data.get("base", ""),
            icon=data.get("icon", ""),
            name=data.get("name", ""),
            open_interest_usd=data.get("openInterestUsd", 0.0),
            symbol=data.get("symbol", ""),
            token_id=data.get("tokenId", ""),
            venues=data.get("venues", 0),
        )


@dataclass
class PremiumDetail:
    bid: str = ""
    # specifies the date and the time in UTC milliseconds
    d: int = 0
    # funding gap which is difference between source and target fundingrate without funding interval consideration
    fg: float = 0.0
    # net fundingrate which takes funding interval into account
    nfr: float = 0.0
    # specifies the price difference percentage between the source and target exchanges
    pdp: float = 0.0
    # specifies the price difference percentage between the source and target exchanges 15m ago
    pdp15m: float = 0.0
    # specifies the price difference percentage between the source and target exchanges 1h ago
    pdp1h: float = 0.0
    # specifies the price difference percentage between the source and target exchanges 24h ago
    pdp24h: float = 0.0
    # specifies the price difference percentage between the source and target exchanges 30m ago
    pdp30m: float = 0.0
    # specifies the price difference percentage between the source and target exchanges 4h ago
    pdp4h: float = 0.0
    # specifies the price difference percentage between the source and target exchanges 5m ago
    pdp5m: float = 0.0
    # sepcifies premium duration
    pmd: int = 0
    # source ask depth within +2% base
    sad: float = 0.0
    # specifies -2% volume depth from source exchange
    sad2p: float = 0.0
    # source ask depth within +2% quote
    sadf: float = 0.0
    # specifies the base token of the source exchange
    sb: str = ""
    # specifies +2% volume depth from source exchange
    sbd2p: float = 0.0
    # for amm source ticker, amm source chain
    sc: Optional[str] = None
    # specifies the source exchange name
    se: str = ""
    # source funding rate
    sfr: float = 0.0
    # source funding rate interval, 1 stands for 1 hour
    sfri: int = 0
    # source fundingrate info timestamp in UTC millisecond
    sfrt: int = 0
    # specifies highest bid from source exchange
    shb: float = 0.0
    # specifies lowest bid from source exchange
    sla: float = 0.0
    # specifies the source market type
    sm: str = ""
    # boolean if source exchange margin is supported, returned only for spot market
    sms: bool = False
    # source next distribution time in UTC milliseconds
    snd: int = 0
    # Open Interest snapshot — USD-denominated. Source and target sides.
    soi: float = 0.0
    # OI % change over rolling 1h / 4h / 24h windows.
    soich1h: float = 0.0
    soich24h: float = 0.0
    soich4h: float = 0.0
    # OI / 24h USD quote volume. Crude "leverage per turnover" metric.
    soivr: float = 0.0
    # specifies the latest price of the source exchange in requested currency
    sp: float = 0.0
    # for amm source ticker, amm pool address
    spa: Optional[str] = None
    # specifies the price difference percentage of the source exchange in the last 15m
    spdp15m: float = 0.0
    # specifies the price difference percentage of the source exchange in the last 1h
    spdp1h: float = 0.0
    # specifies the price difference percentage of the source exchange in the last 24h
    spdp24h: float = 0.0
    # specifies the price difference percentage of the source exchange in the last 30m
    spdp30m: float = 0.0
    # specifies the price difference percentage of the source exchange in the last 4h
    spdp4h: float = 0.0
    # specifies the price difference percentage of the source exchange in the last 5m
    spdp5m: float = 0.0
    # specifies the quote token of the source exchange
    sq: str = ""
    # specifies the date and the time of source ticker in UTC milliseconds
    st: int = 0
    # specifies the trading volume of the source exchange in the last 24 hours in requested currency
    sv: float = 0.0
    # transferable, null if unknown
    t: bool = False
    # specifies -2% volume depth from target exchange
    tad2p: float = 0.0
    # specifies the base token of the target exchange
    tb: str = ""
    # target bid depth within -2% base
    tbd: float = 0.0
    # specifies +2% volume depth from target exchange
    tbd2p: float = 0.0
    # target bid depth within -2% quote
    tbdf: float = 0.0
    # for amm target ticker, amm target chain
    tc: Optional[str] = None
    # specifies the target exchange name
    te: str = ""
    # target funding rate
    tfr: float = 0.0
    # target funding rate interval, 1 stands for 1 hour
    tfri: int = 0
    # target fundingrate info timestamp in UTC millisecond
    tfrt: int = 0
    # specifies highest bid from target exchange
    thb: float = 0.0
    # specifies lowest bid from target exchange
    tla: float = 0.0
    # specifies the target market type
    tm: str = ""
    # boolean if target exchange margin is supported, returned only for spot market
    tms: bool = False
    # target next distribution time in UTC millisconds
    tnd: int = 0
    toi: float = 0.0
    toich1h: float = 0.0
    toich24h: float = 0.0
    toich4h: float = 0.0
    toivr: float = 0.0
    # specifies the latest price of the target exchange
    tp: float = 0.0
    # for amm target ticker, amm pool address
    tpa: Optional[str] = None
    # specifies the price difference percentage of the target exchange in the last 15m
    tpdp15m: float = 0.0
    # specifies the price difference percentage of the target exchange in the last 1h
    tpdp1h: float = 0.0
    # specifies the price difference percentage of the target exchange in the last 24h
    tpdp24h: float = 0.0
    # specifies the price difference percentage of the target exchange in the last 30m
    tpdp30m: float = 0.0
    # specifies the price difference percentage of the target exchange in the last 4h
    tpdp4h: float = 0.0
    # specifies the price difference percentage of the target exchange in the last 5m
    tpdp5m: float = 0.0
    # specifies the quote token of the target exchange
    tq: str = ""
    # specifies the date and the time of target ticker in UTC milliseconds
    tt: int = 0
    # specifies the trading volume of the target exchange in the last 24 hours in requested currency
    tv: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> PremiumDetail:
        return cls(
            bid=data.get("bid", ""),
            d=data.get("d", 0),
            fg=data.get("fg", 0.0),
            nfr=data.get("nfr", 0.0),
            pdp=data.get("pdp", 0.0),
            pdp15m=data.get("pdp15m", 0.0),
            pdp1h=data.get("pdp1h", 0.0),
            pdp24h=data.get("pdp24h", 0.0),
            pdp30m=data.get("pdp30m", 0.0),
            pdp4h=data.get("pdp4h", 0.0),
            pdp5m=data.get("pdp5m", 0.0),
            pmd=data.get("pmd", 0),
            sad=data.get("sad", 0.0),
            sad2p=data.get("sad2p", 0.0),
            sadf=data.get("sadf", 0.0),
            sb=data.get("sb", ""),
            sbd2p=data.get("sbd2p", 0.0),
            sc=data.get("sc"),
            se=data.get("se", ""),
            sfr=data.get("sfr", 0.0),
            sfri=data.get("sfri", 0),
            sfrt=data.get("sfrt", 0),
            shb=data.get("shb", 0.0),
            sla=data.get("sla", 0.0),
            sm=data.get("sm", ""),
            sms=data.get("sms", False),
            snd=data.get("snd", 0),
            soi=data.get("soi", 0.0),
            soich1h=data.get("soich1h", 0.0),
            soich24h=data.get("soich24h", 0.0),
            soich4h=data.get("soich4h", 0.0),
            soivr=data.get("soivr", 0.0),
            sp=data.get("sp", 0.0),
            spa=data.get("spa"),
            spdp15m=data.get("spdp15m", 0.0),
            spdp1h=data.get("spdp1h", 0.0),
            spdp24h=data.get("spdp24h", 0.0),
            spdp30m=data.get("spdp30m", 0.0),
            spdp4h=data.get("spdp4h", 0.0),
            spdp5m=data.get("spdp5m", 0.0),
            sq=data.get("sq", ""),
            st=data.get("st", 0),
            sv=data.get("sv", 0.0),
            t=data.get("t", False),
            tad2p=data.get("tad2p", 0.0),
            tb=data.get("tb", ""),
            tbd=data.get("tbd", 0.0),
            tbd2p=data.get("tbd2p", 0.0),
            tbdf=data.get("tbdf", 0.0),
            tc=data.get("tc"),
            te=data.get("te", ""),
            tfr=data.get("tfr", 0.0),
            tfri=data.get("tfri", 0),
            tfrt=data.get("tfrt", 0),
            thb=data.get("thb", 0.0),
            tla=data.get("tla", 0.0),
            tm=data.get("tm", ""),
            tms=data.get("tms", False),
            tnd=data.get("tnd", 0),
            toi=data.get("toi", 0.0),
            toich1h=data.get("toich1h", 0.0),
            toich24h=data.get("toich24h", 0.0),
            toich4h=data.get("toich4h", 0.0),
            toivr=data.get("toivr", 0.0),
            tp=data.get("tp", 0.0),
            tpa=data.get("tpa"),
            tpdp15m=data.get("tpdp15m", 0.0),
            tpdp1h=data.get("tpdp1h", 0.0),
            tpdp24h=data.get("tpdp24h", 0.0),
            tpdp30m=data.get("tpdp30m", 0.0),
            tpdp4h=data.get("tpdp4h", 0.0),
            tpdp5m=data.get("tpdp5m", 0.0),
            tq=data.get("tq", ""),
            tt=data.get("tt", 0),
            tv=data.get("tv", 0.0),
        )


@dataclass
class PremiumResponse:
    conversion_base: str = ""
    currency: str = ""
    data: List[PremiumView] = field(default_factory=list)
    key: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    total: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> PremiumResponse:
        return cls(
            conversion_base=data.get("conversion_base", ""),
            currency=data.get("currency", ""),
            data=_as_models(PremiumView, data.get("data")),
            key=data.get("key", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            total=data.get("total", 0),
        )


@dataclass
class PremiumView:
    detail: Optional[PremiumDetail] = None
    source_annualized_funding_rate: float = 0.0
    target_annualized_funding_rate: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> PremiumView:
        return cls(
            detail=_as_model(PremiumDetail, data.get("detail")),
            source_annualized_funding_rate=data.get(
                "source_annualized_funding_rate", 0.0
            ),
            target_annualized_funding_rate=data.get(
                "target_annualized_funding_rate", 0.0
            ),
        )


@dataclass
class TelegramChannelsResponse:
    category: str = ""
    data: List[TelegramChannelsView] = field(default_factory=list)
    key: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    total: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> TelegramChannelsResponse:
        return cls(
            category=data.get("category", ""),
            data=_as_models(TelegramChannelsView, data.get("data")),
            key=data.get("key", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            total=data.get("total", 0),
        )


@dataclass
class TelegramChannelsView:
    # specifies the channel category
    category: str = ""
    # specifies the channel name
    channel_name: str = ""
    # specifies the channel title
    channel_title: str = ""
    # specifies the creation time of the channel
    created_at: Optional[int] = None
    # specifies the channel description
    description: str = ""
    # specifies the channel link
    link: str = ""
    # specifies the number of subscribers
    subscribers: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> TelegramChannelsView:
        return cls(
            category=data.get("category", ""),
            channel_name=data.get("channelName", ""),
            channel_title=data.get("channelTitle", ""),
            created_at=data.get("createdAt"),
            description=data.get("description", ""),
            link=data.get("link", ""),
            subscribers=data.get("subscribers", 0),
        )


@dataclass
class TelegramMessagesResponse:
    category: str = ""
    # specifies an array of the Telegram messages
    data: List[TelegramMessagesView] = field(default_factory=list)
    key: str = ""
    limit: int = 0
    page: int = 0
    sort: str = ""
    total: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> TelegramMessagesResponse:
        return cls(
            category=data.get("category", ""),
            data=_as_models(TelegramMessagesView, data.get("data")),
            key=data.get("key", ""),
            limit=data.get("limit", 0),
            page=data.get("page", 0),
            sort=data.get("sort", ""),
            total=data.get("total", 0),
        )


@dataclass
class TelegramMessagesView:
    # specifies the channel handle
    channel_handle: str = ""
    # specifies the channel id
    channel_id: str = ""
    # specifies the channel name
    channel_name: str = ""
    # specifies the number of forwards
    forwards: int = 0
    # specifies the message text
    message: str = ""
    # specifies the message id
    message_id: str = ""
    # specifies the link to Telegram message
    message_link: str = ""
    # specifies the published date
    published_at: int = 0
    # specifies the number of reactions
    reactions: int = 0
    # specifies the number of views
    views: int = 0

    @classmethod
    def from_dict(cls, data: dict) -> TelegramMessagesView:
        return cls(
            channel_handle=data.get("channelHandle", ""),
            channel_id=data.get("channelId", ""),
            channel_name=data.get("channelName", ""),
            forwards=data.get("forwards", 0),
            message=data.get("message", ""),
            message_id=data.get("messageId", ""),
            message_link=data.get("messageLink", ""),
            published_at=data.get("publishedAt", 0),
            reactions=data.get("reactions", 0),
            views=data.get("views", 0),
        )


@dataclass
class TickerResponse:
    currency: str = ""
    data: Optional[TickerView] = None
    market: str = ""
    # Source is populated only when ?include_source=true; omitempty drops the key for default callers, preserving the pre-Phase-1 JSON byte shape (strict-decoder safe).
    src: Any = None

    @classmethod
    def from_dict(cls, data: dict) -> TickerResponse:
        return cls(
            currency=data.get("currency", ""),
            data=_as_model(TickerView, data.get("data")),
            market=data.get("market", ""),
            src=data.get("src"),
        )


@dataclass
class TickerView:
    # specifies the base token
    b: str = ""
    # specifies the date and the time in UTC milliseconds
    d: int = 0
    # specifies the exchange name
    e: str = ""
    # highest bid from orderbook
    hb: float = 0.0
    # lowest ask from orderbook
    la: float = 0.0
    # lower depth(2%)
    ld: float = 0.0
    # specifies the market type
    m: str = ""
    # specifies the latest price
    p: float = 0.0
    # specifies the price 24 hours ago
    p24h: float = 0.0
    # specified price change between the latest price and the price 24 hours ago
    pc: float = 0.0
    # specifies the quote token
    q: str = ""
    # specifies the symbol (base-quote)
    s: str = ""
    # upper depth(2%)
    ud: float = 0.0
    # specifies the trading volume in the last 24 hours
    v: float = 0.0

    @classmethod
    def from_dict(cls, data: dict) -> TickerView:
        return cls(
            b=data.get("b", ""),
            d=data.get("d", 0),
            e=data.get("e", ""),
            hb=data.get("hb", 0.0),
            la=data.get("la", 0.0),
            ld=data.get("ld", 0.0),
            m=data.get("m", ""),
            p=data.get("p", 0.0),
            p24h=data.get("p24h", 0.0),
            pc=data.get("pc", 0.0),
            q=data.get("q", ""),
            s=data.get("s", ""),
            ud=data.get("ud", 0.0),
            v=data.get("v", 0.0),
        )


@dataclass
class TokenDetail:
    # specifies cmc id of the token
    cmc_id: str = ""
    # specifies the token icon url path
    icon: str = ""
    # specifies the unique id
    id: str = ""
    # specifies the name of token
    name: str = ""
    # specifies the token symbol
    symbol: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> TokenDetail:
        return cls(
            cmc_id=data.get("cmc_id", ""),
            icon=data.get("icon", ""),
            id=data.get("id", ""),
            name=data.get("name", ""),
            symbol=data.get("symbol", ""),
        )
