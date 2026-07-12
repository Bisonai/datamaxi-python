"""
Auto-generated WebSocket message models from the datamaxi-backend WS surface.
DO NOT EDIT — regenerate with: make ws-python

Source: pkg/apiws/app.go route table + protobuf/*.proto + Go view structs.
The subscribe `param` formats come from overrides/ws_channels.json (the one
piece not derivable from those sources — see parse_ws.py).
"""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict  # noqa: F401


# source: asyncapi:payload
ForexMessage = TypedDict(
    "ForexMessage",
    {
        "d": int,
        "r": float,
        "s": str,
    },
    total=False,
)


# source: asyncapi:payload
FundingRateMessage = TypedDict(
    "FundingRateMessage",
    {
        "b": str,
        "d": int,
        "e": str,
        "f": float,
        "i": int,
        "id": str,
        "q": str,
        "s": str,
    },
    total=False,
)


# source: asyncapi:payload
LiquidationMessage = TypedDict(
    "LiquidationMessage",
    {
        "b": str,
        "d": int,
        "e": str,
        "id": str,
        "p": float,
        "pfiat": float,
        "pusd": float,
        "q": str,
        "s": str,
        "sd": str,
        "snap": bool,
        "v": float,
        "vfiat": float,
        "vusd": float,
    },
    total=False,
)


# source: asyncapi:payload
ListingMessage = TypedDict(
    "ListingMessage",
    {
        "b": str,
        "d": int,
        "e": str,
        "q": str,
        "u": str,
    },
    total=False,
)


# source: asyncapi:payload
OpenInterestMessage = TypedDict(
    "OpenInterestMessage",
    {
        "b": str,
        "d": int,
        "e": str,
        "id": str,
        "oi": float,
        "oifiat": float,
        "oiusd": float,
        "q": str,
        "s": str,
    },
    total=False,
)


# source: asyncapi:payload
PremiumMessage = TypedDict(
    "PremiumMessage",
    {
        "key": str,
        "premium": float,
        "source_base": str,
        "source_exchange": str,
        "source_market": str,
        "source_price": float,
        "source_quote": str,
        "target_exchange": str,
        "target_market": str,
        "target_price": float,
        "target_quote": str,
        "timestamp": int,
        "token_id": str,
    },
    total=False,
)


# source: asyncapi:payload
TickerMessage = TypedDict(
    "TickerMessage",
    {
        "b": str,
        "d": int,
        "e": str,
        "hb": float,
        "la": float,
        "ld": float,
        "m": str,
        "p": float,
        "p24h": float,
        "pc": float,
        "q": str,
        "s": str,
        "ud": float,
        "v": float,
    },
    total=False,
)
