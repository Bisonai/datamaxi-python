"""
Auto-generated WebSocket channel registry from the datamaxi-backend WS surface.
DO NOT EDIT — regenerate with: make ws-python

Source: pkg/apiws/app.go route table + protobuf/*.proto + Go view structs.
The subscribe `param` formats come from overrides/ws_channels.json (the one
piece not derivable from those sources — see parse_ws.py).
"""

WS_BASE_PATH = "/ws/v1"
WS_AUTH_HEADER = "X-DTMX-APIKEY"

WS_CHANNELS = {
    "/announcement/listing": {
        "plan": "pro_plus",
        "market": None,
        "message": "ListingMessage",
        "param": None,
        "subscribe": True,
        "unsubscribe": True,
    },
    "/announcement/listing/internal": {
        "plan": "pro_plus",
        "market": None,
        "message": "InternalListingMessage",
        "param": None,
        "subscribe": True,
        "unsubscribe": True,
    },
    "/forex": {
        "plan": "basic",
        "market": None,
        "message": "ForexMessage",
        "param": "SYMBOL",
        "subscribe": True,
        "unsubscribe": True,
    },
    "/front/liquidation/feed": {
        "plan": "front",
        "market": None,
        "message": "LiquidationMessage",
        "param": None,
        "subscribe": False,
        "unsubscribe": False,
    },
    "/front/listing/deposit": {
        "plan": "front",
        "market": None,
        "message": "DepositListingMessage",
        "param": None,
        "subscribe": True,
        "unsubscribe": True,
    },
    "/funding-rate": {
        "plan": "basic",
        "market": None,
        "message": "FundingRateMessage",
        "param": "SYMBOL@exchange",
        "subscribe": True,
        "unsubscribe": True,
    },
    "/liquidation": {
        "plan": "basic",
        "market": None,
        "message": "LiquidationMessage",
        "param": "SYMBOL@exchange",
        "subscribe": True,
        "unsubscribe": False,
    },
    "/liquidation/feed": {
        "plan": "basic",
        "market": None,
        "message": "LiquidationMessage",
        "param": None,
        "subscribe": False,
        "unsubscribe": False,
    },
    "/open-interest": {
        "plan": "basic",
        "market": None,
        "message": "OpenInterestMessage",
        "param": "SYMBOL@exchange",
        "subscribe": True,
        "unsubscribe": False,
    },
    "/premium": {
        "plan": "basic",
        "market": None,
        "message": "PremiumMessage",
        "param": "src:tgt:tokenId:srcQuote:tgtQuote:srcMkt:tgtMkt",
        "subscribe": True,
        "unsubscribe": True,
    },
    "/ticker/futures": {
        "plan": "basic",
        "market": "futures",
        "message": "TickerMessage",
        "param": "SYMBOL@exchange[@currency@conversionBase]",
        "subscribe": True,
        "unsubscribe": True,
    },
    "/ticker/spot": {
        "plan": "basic",
        "market": "spot",
        "message": "TickerMessage",
        "param": "SYMBOL@exchange[@currency@conversionBase]",
        "subscribe": True,
        "unsubscribe": True,
    },
}
