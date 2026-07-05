"""
Auto-generated WebSocket message models from the datamaxi-backend WS surface.
DO NOT EDIT — regenerate with: make ws-python

Source: pkg/apiws/app.go route table + protobuf/*.proto + Go view structs.
The subscribe `param` formats come from overrides/ws_channels.json (the one
piece not derivable from those sources — see parse_ws.py).
"""

from __future__ import annotations

from typing import Any, Dict, List, TypedDict  # noqa: F401


# source: gostruct:pkg/apiforex/app.go::Forex
ForexMessage = TypedDict(
    "ForexMessage",
    {
        "s": str,
        "d": int,
        "r": float,
    },
    total=False,
)


# source: gostruct:pkg/apifundingrate/types.go::Snapshot
FundingRateMessage = TypedDict(
    "FundingRateMessage",
    {
        "f": float,
        "i": int,
        "e": str,
        "id": str,
        "s": str,
        "b": str,
        "q": str,
        "d": int,
        "p": int,
    },
    total=False,
)


# source: gostruct:pkg/apiannouncement/app.go::InternalListing
InternalListingMessage = TypedDict(
    "InternalListingMessage",
    {
        "s": str,
        "e": str,
        "b": str,
        "t": str,
        "u": str,
        "d": int,
    },
    total=False,
)


# source: proto:protobuf/liquidation.proto::liquidation
LiquidationMessage = TypedDict(
    "LiquidationMessage",
    {
        "id": str,
        "e": str,
        "d": str,
        "s": str,
        "b": str,
        "q": str,
        "sd": str,
        "p": float,
        "pusd": float,
        "pfiat": float,
        "v": float,
        "vusd": float,
        "vfiat": float,
        "pt": Dict[str, Any],
        "pa": str,
        "src": Any,
    },
    total=False,
)


# source: gostruct:pkg/apiannouncement/app.go::Listing
ListingMessage = TypedDict(
    "ListingMessage",
    {
        "e": str,
        "b": str,
        "q": str,
        "u": str,
        "d": int,
    },
    total=False,
)


# source: proto:protobuf/open-interest.proto::open_interest
OpenInterestMessage = TypedDict(
    "OpenInterestMessage",
    {
        "id": str,
        "e": str,
        "d": str,
        "s": str,
        "b": str,
        "q": str,
        "oi": float,
        "oiusd": float,
        "oifiat": float,
        "pt": Dict[str, Any],
        "pa": str,
    },
    total=False,
)


# source: gostruct:pkg/apipremium/handlers/dataapipremiumws/handler.go::PremiumOut
PremiumMessage = TypedDict(
    "PremiumMessage",
    {
        "key": str,
        "source_exchange": str,
        "target_exchange": str,
        "token_id": str,
        "source_base": str,
        "source_quote": str,
        "target_quote": str,
        "source_market": str,
        "target_market": str,
        "premium": float,
        "source_price": float,
        "target_price": float,
        "timestamp": int,
    },
    total=False,
)


# source: gostruct:pkg/apiticker/app.go::View
TickerMessage = TypedDict(
    "TickerMessage",
    {
        "p": float,
        "v": float,
        "p24h": float,
        "pc": float,
        "hb": float,
        "la": float,
        "ud": float,
        "ld": float,
        "e": str,
        "s": str,
        "b": str,
        "q": str,
        "d": int,
        "m": str,
    },
    total=False,
)
