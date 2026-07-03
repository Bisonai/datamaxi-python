"""Typed response models (pilot — see #141).

These describe the raw JSON returned on the ``pandas=False`` path of the
candle and ticker endpoints. They are hint-only ``TypedDict``s (no runtime
cost, no validation) so callers get IDE autocomplete / mypy checking on the
dict shape without any behavior change.

Wire note: numeric fields arrive as **strings** (e.g. ``"105.5"``), and a
missing value arrives as the literal string ``"NaN"``. The ``pandas=True``
path coerces these to numbers; the raw dict below preserves them as strings.

This is a deliberately small pilot; other endpoints can be typed the same way
incrementally.
"""

from typing import List, TypedDict


class CandleRow(TypedDict):
    """One candle from the ``data`` array of ``GET /api/v1/cex/candle``."""

    d: str  # candle open time, UTC milliseconds
    o: str  # open price
    h: str  # high price
    l: str  # low price
    c: str  # close price
    v: str  # trading volume (base token)


class CandleResponse(TypedDict):
    """Raw envelope returned by ``cex.candle(..., pandas=False)``."""

    data: List[CandleRow]


class TickerData(TypedDict):
    """The ``data`` object of ``GET /api/v1/ticker``."""

    b: str  # base token
    d: str  # timestamp, UTC milliseconds
    e: str  # exchange name
    hb: str  # highest bid (orderbook)
    la: str  # lowest ask (orderbook)
    ld: str  # lower depth (2%)
    m: str  # market type (spot/futures)
    p: str  # latest price
    p24h: str  # price 24 hours ago
    pc: str  # price change vs 24h ago
    q: str  # quote token
    s: str  # symbol (base-quote)
    ud: str  # upper depth (2%)
    v: str  # 24h trading volume


class TickerResponse(TypedDict):
    """Raw envelope returned by ``cex.ticker.get(..., pandas=False)``."""

    data: TickerData
