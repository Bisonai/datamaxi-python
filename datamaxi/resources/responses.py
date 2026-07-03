"""Typed response models (see #141).

Hint-only ``TypedDict``s describing the raw ``pandas=False`` JSON returned by
the data endpoints, so callers get IDE autocomplete / mypy checking on the
dict shape with no runtime cost, no validation, and no behavior change.

Conventions
-----------
* Field names and presence are taken from the live API docs
  (docs.datamaxiplus.com).
* Fields are typed ``str`` because this API serializes JSON values as strings
  on the wire — verified for candle / ticker / funding (string mocks + the
  ``convert_data_to_data_frame`` coercion, where a missing value arrives as
  the literal string ``"NaN"``). The ``pandas=True`` path coerces numerics.
  Two documented exceptions are typed natively: booleans (e.g. premium
  ``t`` / ``sms`` / ``tms``) and Naver-trend ``v`` (an integer on the wire).
* These are hand-authored, so they can drift if the backend changes; a
  drift-proof version would emit them from the upstream OpenAPI codegen.

Envelope vs bare: some endpoints wrap rows in ``{"data": [...]}`` (typed as a
``*Response``), some return a bare list, and some a single object — each
method's annotation matches its actual ``pandas=False`` return.
"""

from typing import List, TypedDict


# --- CEX candle -------------------------------------------------------------
class CandleRow(TypedDict):
    """One candle from ``GET /api/v1/cex/candle``."""

    d: str  # candle open time, UTC milliseconds
    o: str  # open price
    h: str  # high price
    l: str  # low price
    c: str  # close price
    v: str  # trading volume (base token)


class CandleResponse(TypedDict):
    """Raw envelope from ``cex.candle(..., pandas=False)``."""

    data: List[CandleRow]


# --- CEX ticker -------------------------------------------------------------
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
    """Raw envelope from ``cex.ticker.get(..., pandas=False)``."""

    data: TickerData


# --- CEX announcements ------------------------------------------------------
class AnnouncementRow(TypedDict):
    """One announcement from ``GET /api/v1/cex/announcement``."""

    c: str  # category
    d: str  # date (UTC ms)
    e: str  # exchange
    s: str  # summary
    t: str  # title
    u: str  # url


class AnnouncementResponse(TypedDict):
    """Raw envelope from ``cex.announcement(...)`` (first tuple element)."""

    data: List[AnnouncementRow]


# --- CEX token updates ------------------------------------------------------
class TokenUpdateRow(TypedDict):
    """One token update from ``GET /api/v1/cex/token-updates``."""

    b: str  # base token
    d: str  # event timestamp (UTC ms)
    e: str  # exchange
    m: str  # market
    q: str  # quote token
    t: str  # update type (listed / delisted)


class TokenUpdateResponse(TypedDict):
    """Raw envelope from ``cex.token.updates(...)`` (first tuple element)."""

    data: List[TokenUpdateRow]


# --- CEX wallet status ------------------------------------------------------
class WalletStatusRow(TypedDict):
    """One wallet/transfer status row from ``GET /api/v1/cex/wallet-status``."""

    currency: str  # asset
    deposit_state: str  # deposit functionality status
    deposit_message: str  # deposit status detail
    withdraw_state: str  # withdrawal functionality status
    withdraw_message: str  # withdrawal status detail
    exchange: str  # CEX name
    network: str  # blockchain network
    updated_at: str  # last-update timestamp


# cex.wallet_status(..., pandas=False) returns a bare List[WalletStatusRow].


# --- Forex ------------------------------------------------------------------
class ForexRow(TypedDict):
    """The forex object from ``GET /api/v1/forex``."""

    d: str  # timestamp (UTC ms)
    r: str  # forex rate
    s: str  # forex symbol


# --- Funding rate -----------------------------------------------------------
class FundingRateRow(TypedDict):
    """One historical funding-rate point (``.funding_rate.history``)."""

    d: str  # timestamp (UTC ms)
    f: str  # funding rate


class FundingHistoryResponse(TypedDict):
    """Raw envelope from ``funding_rate.history(...)`` (first tuple element)."""

    data: List[FundingRateRow]


class LatestFundingRate(TypedDict):
    """The single object from ``funding_rate.latest(...)``."""

    b: str  # base asset
    d: str  # timestamp
    e: str  # exchange
    f: str  # funding rate
    i: str  # interval (hours)
    id: str  # token identifier
    p: str  # processed timestamp
    q: str  # quote asset
    s: str  # symbol


# --- Premium ----------------------------------------------------------------
class PremiumDetail(TypedDict, total=False):
    """Per-pair premium detail (``item["detail"]``).

    ``total=False``: AMM-only fields (chain / pool address) and other optional
    metrics are absent for many pairs.
    """

    bid: str  # base token identifier
    d: str  # timestamp (UTC ms)
    fg: str  # source-minus-target funding-rate diff
    nfr: str  # net funding rate (interval-adjusted)
    pdp: str  # current price difference %
    pdp1h: str  # price difference % 1h ago
    pdp4h: str  # price difference % 4h ago
    pdp5m: str  # price difference % 5m ago
    pdp15m: str  # price difference % 15m ago
    pdp24h: str  # price difference % 24h ago
    pdp30m: str  # price difference % 30m ago
    pmd: str  # premium duration
    sad: str  # source ask depth within +2%
    sad2p: str  # source -2% volume depth
    sadf: str  # source ask depth within +2% (quote)
    sb: str  # source base token
    sbd2p: str  # source +2% volume depth
    sc: str  # source chain (AMM)
    se: str  # source exchange
    sfr: str  # source funding rate
    sfri: str  # source funding-rate interval (hours)
    sfrt: str  # source funding-rate timestamp (UTC ms)
    shb: str  # source highest bid
    sla: str  # source lowest ask
    sm: str  # source market type (spot/futures)
    sms: bool  # source margin support
    snd: str  # source next distribution time (UTC ms)
    soi: str  # source open interest (USD)
    soich1h: str  # source OI % change (1h)
    soich4h: str  # source OI % change (4h)
    soich24h: str  # source OI % change (24h)
    soivr: str  # source OI/volume ratio
    sp: str  # source latest price
    spa: str  # source pool address (AMM)
    spdp1h: str  # source price change (1h)
    spdp4h: str  # source price change (4h)
    spdp5m: str  # source price change (5m)
    spdp15m: str  # source price change (15m)
    spdp24h: str  # source price change (24h)
    spdp30m: str  # source price change (30m)
    sq: str  # source quote token
    st: str  # source ticker timestamp (UTC ms)
    sv: str  # source 24h volume
    t: bool  # transferable
    tad2p: str  # target -2% volume depth
    tb: str  # target base token
    tbd: str  # target bid depth within -2%
    tbd2p: str  # target +2% volume depth
    tbdf: str  # target bid depth within -2% (quote)
    tc: str  # target chain (AMM)
    te: str  # target exchange
    tfr: str  # target funding rate
    tfri: str  # target funding-rate interval (hours)
    tfrt: str  # target funding-rate timestamp (UTC ms)
    thb: str  # target highest bid
    tla: str  # target lowest ask
    tm: str  # target market type (spot/futures)
    tms: bool  # target margin support
    tnd: str  # target next distribution time (UTC ms)
    toi: str  # target open interest (USD)
    toich1h: str  # target OI % change (1h)
    toich4h: str  # target OI % change (4h)
    toich24h: str  # target OI % change (24h)
    toivr: str  # target OI/volume ratio
    tp: str  # target latest price
    tpa: str  # target pool address (AMM)
    tpdp1h: str  # target price change (1h)
    tpdp4h: str  # target price change (4h)
    tpdp5m: str  # target price change (5m)
    tpdp15m: str  # target price change (15m)
    tpdp24h: str  # target price change (24h)
    tpdp30m: str  # target price change (30m)
    tq: str  # target quote token
    tt: str  # target ticker timestamp (UTC ms)
    tv: str  # target 24h volume


class PremiumRow(TypedDict):
    """One item from the premium ``data`` array."""

    detail: PremiumDetail
    source_annualized_funding_rate: str
    target_annualized_funding_rate: str


class PremiumResponse(TypedDict):
    """Raw envelope from ``premium(..., pandas=False)``."""

    data: List[PremiumRow]


# --- Telegram ---------------------------------------------------------------
class TelegramChannel(TypedDict):
    """One channel from ``GET /api/v1/telegram/channels``."""

    category: str
    channelName: str
    channelTitle: str
    createdAt: str  # creation time
    description: str
    link: str
    subscribers: str  # subscriber count


class TelegramChannelsResponse(TypedDict):
    """Raw envelope from ``telegram.channels(...)`` (first tuple element)."""

    data: List[TelegramChannel]


class TelegramMessage(TypedDict):
    """One message from ``GET /api/v1/telegram/messages``."""

    channelHandle: str
    channelId: str
    channelName: str
    forwards: str  # forward count
    message: str  # message text
    messageId: str
    messageLink: str
    publishedAt: str  # published date
    reactions: str  # reaction count
    views: str  # view count


class TelegramMessagesResponse(TypedDict):
    """Raw envelope from ``telegram.messages(...)`` (first tuple element)."""

    data: List[TelegramMessage]


# --- Naver trend ------------------------------------------------------------
class NaverTrendRow(TypedDict):
    """One Naver-trend point from ``GET /api/v1/naver-trend``."""

    d: str  # date
    v: int  # trend value (native integer on the wire)


# naver.trend(..., pandas=False) returns a bare List[NaverTrendRow].
