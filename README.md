# DataMaxi+ Python SDK

[![PyPI version](https://img.shields.io/pypi/v/datamaxi)](https://pypi.python.org/pypi/datamaxi)
[![Python version](https://img.shields.io/pypi/pyversions/datamaxi)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://datamaxi.readthedocs.io/en/stable/)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [DataMaxi+ API](https://docs.datamaxiplus.com/) —
one library for both **historical** and **real-time** crypto market data.

- **REST** — OHLCV candles, tickers, trading fees, wallet status, announcements
  and token updates across centralized exchanges; perpetual funding rates,
  liquidations, open interest, margin-borrow rates; cross-exchange price
  premiums for arbitrage; index prices and forex rates; Telegram channel data
  and Naver search trends.
- **WebSocket** — stream tickers, forex, premiums, funding rates, open interest,
  liquidations and listing announcements as they happen.
- **Sync or async** — a synchronous client, a coroutine-based async twin, and an
  async WebSocket client, all sharing the same resource tree and arguments.

Compatible with Python v3.10+.

## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [Quickstart](#quickstart)
- [Clients](#clients)
- [REST API Reference](#rest-api-reference)
  - [CEX](#cex) — [Candle](#cex-candle-data), [Ticker](#cex-ticker-data), [Fees](#cex-trading-fees), [Wallet Status](#cex-wallet-status), [Announcements](#cex-announcements), [Token Updates](#cex-token-updates), [Symbol](#cex-symbol)
  - [Derivatives and Leverage](#derivatives-and-leverage) — [Funding Rate](#funding-rate), [Liquidation](#liquidation), [Open Interest](#open-interest), [Margin Borrow](#margin-borrow)
  - [Pricing and Cross-Exchange](#pricing-and-cross-exchange) — [Premium](#premium), [Index Price](#index-price), [Forex](#forex)
  - [Alternative Data](#alternative-data) — [Telegram](#telegram), [Naver Trend](#naver-trend)
- [WebSockets](#websockets)
- [Response Types](#response-types)
- [Pagination](#pagination)
- [Error Handling](#error-handling)
- [Async Client](#async-client)
- [Local Development](#local-development)
- [Tests](#tests)
- [Links](#links)
- [Contributing](#contributing)
- [License](#license)

## Installation

```shell
pip install datamaxi
```

The SDK is lightweight by default (`requests` + `pandas`). Two features live
behind optional extras so you only install what you use:

| Extra                           | Installs     | Enables                                          |
| ------------------------------- | ------------ | ------------------------------------------------ |
| `pip install "datamaxi[async]"` | `httpx`      | The async client, [`AsyncDatamaxi`](#async-client). |
| `pip install "datamaxi[ws]"`    | `websockets` | The async WebSocket client, [`AsyncDatamaxiWS`](#websockets). |

Combine them in one shot: `pip install "datamaxi[async,ws]"`.

## Authentication

DataMaxi+ endpoints are protected by an API key. Get one by registering at
https://datamaxiplus.com/auth.

Set it once via the `DATAMAXI_API_KEY` environment variable (recommended, so the
key stays out of source code) and every client picks it up automatically:

```shell
export DATAMAXI_API_KEY="your_api_key"
```

Or pass it explicitly to any client: `Datamaxi(api_key="your_api_key")`.

Every client accepts the following options:

| Option             | Explanation                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| `api_key`          | Your API key. Falls back to `DATAMAXI_API_KEY` when omitted.                           |
| `base_url`         | API base URL. Defaults to `https://api.datamaxiplus.com`.                             |
| `timeout`          | Seconds to wait for a server response. By default requests do not time out.           |
| `proxies`          | Proxy through which the request is routed.                                             |
| `show_limit_usage` | *(Deprecated)* Return a dict with `"limit_usage"` and `"data"` keys. See [Response Types](#response-types). |
| `show_header`      | *(Deprecated)* Return a dict with `"header"` and `"data"` keys. See [Response Types](#response-types). |

### Environment Variables

| Env                | Description                                  |
| ------------------ | -------------------------------------------- |
| `DATAMAXI_API_KEY` | Used instead of `api_key` if none is passed. |

## Quickstart

Set `DATAMAXI_API_KEY` (see [Authentication](#authentication)), then pick the
style that fits your app — synchronous, `asyncio`, or streaming over WebSocket.
All three share the same resource tree, so an endpoint you learn in one works in
the others.

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

# The client reads DATAMAXI_API_KEY from the environment automatically.
# Alternatively, pass api_key="your_api_key" explicitly.
maxi = Datamaxi()

# Telegram and Naver are mounted as `maxi.telegram` / `maxi.naver`
# (standalone `Telegram` / `Naver` clients remain available too).
channels, _ = maxi.telegram.channels()
trend = maxi.naver.trend(symbol="BTC")

# Fetch CEX candle data (returns pandas DataFrame)
df = maxi.cex.candle(
    exchange="binance",
    symbol="BTC-USDT",
    interval="1d",
    market="spot",
)
print(df.head())

# Fetch ticker data
ticker = maxi.cex.ticker.get(exchange="binance", symbol="BTC-USDT", market="spot")
print(ticker)

# Fetch premium data
premium = maxi.premium(asset="BTC")
print(premium.head())
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    # Reads DATAMAXI_API_KEY from the environment automatically.
    # Alternatively, pass api_key="your_api_key" explicitly.
    async with AsyncDatamaxi() as client:
        df = await client.cex.candle(
            exchange="binance", symbol="BTC-USDT", interval="1d", market="spot"
        )
        print(df.head())

        ticker = await client.cex.ticker.get(
            exchange="binance", symbol="BTC-USDT", market="spot"
        )
        print(ticker)

        premium = await client.premium(asset="BTC")
        print(premium.head())


asyncio.run(main())
```

</details>

<details markdown="1"><summary>WebSocket</summary>

Requires the `ws` extra (`pip install "datamaxi[ws]"`). Streaming is
async-only — see [WebSockets](#websockets) for the full channel list.

```python
import asyncio
from datamaxi.aio.ws import AsyncDatamaxiWS


async def main():
    # Reads DATAMAXI_API_KEY from the environment automatically.
    async with AsyncDatamaxiWS() as ws:
        # subscribe() returns an async iterator over live messages
        async for msg in await ws.ticker.subscribe("BTC-USDT@binance", market="spot"):
            print(msg["s"], msg.get("p"))  # symbol, price


asyncio.run(main())
```

</details>

## Clients

The package ships these clients, all configured the same way (see
[Authentication](#authentication)):

| Client            | Import                                        | Purpose                                                    |
| ----------------- | --------------------------------------------- | ---------------------------------------------------------- |
| `Datamaxi`        | `from datamaxi import Datamaxi`               | Synchronous client for all REST data, incl. `maxi.telegram` / `maxi.naver`. |
| `Telegram`        | `from datamaxi import Telegram`               | Standalone Telegram client (also mounted as `maxi.telegram`). |
| `Naver`           | `from datamaxi import Naver`                  | Standalone Naver search-trend client (also mounted as `maxi.naver`). |
| `AsyncDatamaxi`   | `from datamaxi.aio import AsyncDatamaxi`      | Async twin of `Datamaxi` (needs the `[async]` extra).      |
| `AsyncDatamaxiWS` | `from datamaxi.aio.ws import AsyncDatamaxiWS` | Async WebSocket streaming (needs the `[ws]` extra).        |

Telegram and Naver are mounted on `Datamaxi` / `AsyncDatamaxi` (`maxi.telegram`,
`maxi.naver`) so they reuse the client's shared session. The standalone
`Telegram` / `Naver` (and their async twins `AsyncTelegram` / `AsyncNaver`,
imported from `datamaxi.aio`) remain available for independent use.

## REST API Reference

> **Discovery helpers.** Most endpoints expose helpers to list valid argument
> values before you fetch — commonly `.exchanges()`, `.symbols(exchange=...)`, and
> (for candles) `.intervals()`. Use them to discover supported exchanges, trading
> pairs, and intervals. The examples below show them per endpoint.

All examples use the sync `Datamaxi` client. Every endpoint works identically on
the [async client](#async-client) — just `await` the call. Each endpoint also has
a dedicated page with a Sync/Async tab in the
[docs](https://datamaxi.readthedocs.io/).

### CEX

Data from centralized exchanges: prices, fees, wallet status, and listings.

#### CEX Candle Data

Fetch historical candlestick (OHLCV) data from centralized exchanges.

```python
# Get supported exchanges
exchanges = maxi.cex.candle.exchanges(market="spot")  # or "futures"

# Get supported symbols for an exchange
symbols = maxi.cex.candle.symbols(exchange="binance", market="spot")

# Get supported intervals
intervals = maxi.cex.candle.intervals()

# Fetch candle data
df = maxi.cex.candle(
    exchange="binance",      # Required: exchange name
    symbol="BTC-USDT",       # Required: trading pair
    interval="1d",           # Required: candle interval (1m, 5m, 15m, 30m, 1h, 4h, 1d)
    market="spot",           # Required: "spot" or "futures"
    currency="USD",          # Optional: price currency (default: USD)
    from_unix=None,          # Optional: start time (unix timestamp)
    to_unix=None,            # Optional: end time (unix timestamp)
    pandas=True              # Optional: return DataFrame (default) or dict
)
```

#### CEX Ticker Data

Fetch real-time ticker data from centralized exchanges.

```python
# Get supported exchanges
exchanges = maxi.cex.ticker.exchanges(market="spot")

# Get supported symbols
symbols = maxi.cex.ticker.symbols(exchange="binance", market="spot")

# Fetch ticker data
ticker = maxi.cex.ticker.get(
    exchange="binance",      # Required: exchange name
    symbol="BTC-USDT",       # Required: trading pair
    market="spot",           # Required: "spot" or "futures"
    currency=None,           # Optional: price currency
    conversion_base=None,    # Optional: conversion base
    pandas=True              # Optional: return DataFrame or dict
)
```

#### CEX Trading Fees

Fetch trading fee information from centralized exchanges.

```python
# Get supported exchanges
exchanges = maxi.cex.fee.exchanges()

# Get supported symbols
symbols = maxi.cex.fee.symbols(exchange="binance")

# Fetch fee data
fees = maxi.cex.fee(
    exchange="binance",      # Required: exchange name
    symbol="BTC-USDT"        # Required: trading pair
)
```

#### CEX Wallet Status

Fetch deposit/withdrawal status for assets on centralized exchanges.

```python
# Get supported exchanges
exchanges = maxi.cex.wallet_status.exchanges()

# Get supported assets
assets = maxi.cex.wallet_status.assets(exchange="binance")

# Fetch wallet status
status = maxi.cex.wallet_status(
    exchange="binance",      # Required: exchange name
    asset="BTC",             # Required: asset symbol
    pandas=True              # Optional: return DataFrame or list
)
```

#### CEX Announcements

Fetch exchange announcements (listings, delistings, etc.).

```python
# Fetch announcements
data, next_request = maxi.cex.announcement(
    page=1,                  # Optional: page number (default: 1)
    limit=1000,              # Optional: items per page (default: 1000)
    sort="desc",             # Optional: "asc" or "desc" (default: desc)
    key=None,                # Optional: sort key
    exchange=None,           # Optional: filter by exchange
    category=None            # Optional: filter by category
)

# Get next page
data2, next_request2 = next_request()
```

#### CEX Token Updates

Fetch token listing/delisting updates.

```python
# Fetch token updates
data, next_request = maxi.cex.token.updates(
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    type=None,               # Optional: "listed" or "delisted"
)
```

#### CEX Symbol

Per-base / per-symbol CEX metadata and aggregates: trading status, tags,
cautions, delistings, volume, open interest, and liquidation.

```python
metadata = maxi.cex.symbol.metadata(exchange="binance", base="BTC")
tags = maxi.cex.symbol.tags(exchange="binance", base="BTC")
cautions = maxi.cex.symbol.cautions(exchange="binance")
delistings = maxi.cex.symbol.delistings(exchange="binance")
volume = maxi.cex.symbol.volume(base="BTC")
oi = maxi.cex.symbol.oi(base="BTC", exchange="binance")
oi_stats = maxi.cex.symbol.oi_stats(base="BTC", exchange="binance", currency="USD")
liquidation = maxi.cex.symbol.liquidation(base="BTC", window="24h")
```

### Derivatives and Leverage

Perpetual funding, liquidations, open interest, and margin-borrow rates.

#### Funding Rate

Fetch funding rate data for perpetual futures.

```python
# Get supported exchanges
exchanges = maxi.funding_rate.exchanges()

# Get supported symbols
symbols = maxi.funding_rate.symbols(exchange="binance")

# Fetch historical funding rates
df, next_request = maxi.funding_rate.history(
    exchange="binance",      # Required: exchange name
    symbol="BTC-USDT",       # Required: trading pair
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    fromDateTime=None,       # Optional: start datetime
    toDateTime=None,         # Optional: end datetime (cannot set both from and to)
    sort="desc",             # Optional: "asc" or "desc"
    pandas=True              # Optional: return DataFrame or dict
)

# Fetch latest funding rate
df = maxi.funding_rate.latest(
    exchange="binance",      # Required: exchange name
    symbol="BTC-USDT",       # Required: trading pair
    sort=None,               # Optional: "asc" or "desc"
    limit=None,              # Optional: limit results
    pandas=True              # Optional: return DataFrame or dict
)
```

#### Liquidation

CEX futures liquidation data: recent events, a firehose feed, heatmaps, maps,
and bucketed history.

```python
events = maxi.liquidation(exchange="binance", symbol="BTC-USDT", limit=100)
feed = maxi.liquidation.feed(limit=100)                       # most recent across all symbols
heatmap = maxi.liquidation.heatmap(window="1h", topN=10)      # window: 1h/4h/24h, topN 1-30
stats = maxi.liquidation.stats(window="1h")
liq_map = maxi.liquidation.map(base="BTC", exchange="binance", quote="USDT")
history = maxi.liquidation.symbol_history(
    symbol="BTC", quote="USDT", exchange="binance", interval="5m", window="24h"
)
```

#### Open Interest

CEX futures open interest: latest snapshots, reporting pairs, the token ×
exchange matrix, top-line aggregates, and aggregated history.

```python
snapshot = maxi.open_interest(exchange="binance", symbol="BTC-USDT")
pairs = maxi.open_interest.list(exchange="binance")
overview = maxi.open_interest.overview(page=1, limit=20, key="binance", sort="desc")
summary = maxi.open_interest.summary(topN=10)
history = maxi.open_interest.history_aggregated(token_id="bitcoin", interval="1h")
```

#### Margin Borrow

Margin-borrow data for a single asset.

```python
data = maxi.margin_borrow(asset="BTC")
```

### Pricing and Cross-Exchange

Cross-exchange premiums, index prices, and forex rates.

#### Premium

Fetch cross-exchange price premium data for arbitrage analysis.

```python
# Get supported exchanges
exchanges = maxi.premium.exchanges()

# Fetch premium data with common filters
df = maxi.premium(
    source_exchange=None,    # Optional: source exchange
    target_exchange=None,    # Optional: target exchange
    asset=None,              # Optional: asset symbol (e.g., "BTC")
    source_market=None,      # Optional: "spot" or "futures"
    target_market=None,      # Optional: "spot" or "futures"
    min_pdp=None,            # Optional: min price difference percentage
    max_pdp=None,            # Optional: max price difference percentage
    token_include=None,      # Optional: include specific tokens (full name, e.g. "bitcoin")
    token_exclude=None,      # Optional: exclude specific tokens (full name, e.g. "bitcoin")
    page=1,                  # Optional: page number
    limit=100,               # Optional: items per page
    sort=None,               # Optional: "asc" or "desc"
    key=None,                # Optional: sort key (e.g., "pdp")
    pandas=True              # Optional: return DataFrame or dict
)
```

`premium()` accepts many additional filters — quote currencies, time-windowed
price-difference thresholds (`min/max_pd`, `pdp24h`/`pdp4h`/`pdp1h`/`pdp30m`/`pdp15m`/`pdp5m`),
volume bounds (`min/max_sv`, `min/max_tv`), funding-rate bounds, `only_transferable`,
`network`, and more. See the [premium endpoint docs](https://docs.datamaxiplus.com/)
for the full list.

#### Index Price

Historical index-price time series for a single asset.

```python
data = maxi.index_price(
    asset="BTC",
    from_="now - 1 month",   # from_ has a trailing underscore (from is a keyword);
    to="now",                # the wire-level query param is still "from"
    interval="5m",
)
```

#### Forex

Fetch forex exchange rate data.

```python
# Get supported symbols
symbols = maxi.forex.symbols()

# Fetch forex data
df = maxi.forex(
    symbol="USD-KRW",        # Required: currency pair
    pandas=True              # Optional: return DataFrame or dict
)
```

### Alternative Data

Off-exchange signals: Telegram channels and Naver search trends.

#### Telegram

Fetch Telegram channel messages and metadata.

```python
# Telegram is mounted on the client as `maxi.telegram`
# (a standalone `from datamaxi import Telegram` client also works).

# Fetch channels
data, next_request = maxi.telegram.channels(
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    category=None,           # Optional: filter by category
    key=None,                # Optional: sort key
    sort="desc"              # Optional: "asc" or "desc"
)

# Fetch messages
data, next_request = maxi.telegram.messages(
    channel_name=None,       # Optional: filter by channel
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    key=None,                # Optional: sort key
    sort="desc",             # Optional: "asc" or "desc"
    category=None            # Optional: filter by category
)
```

#### Naver Trend

Fetch Naver search trend data (South Korea).

```python
# Naver is mounted on the client as `maxi.naver`
# (a standalone `from datamaxi import Naver` client also works).

# Get supported symbols
symbols = maxi.naver.symbols()

# Fetch trend data
data = maxi.naver.trend(
    symbol="BTC",            # Required: symbol to search
    pandas=True              # Optional: return DataFrame or list
)
```

## WebSockets

Stream real-time market data over the DataMaxi+ WebSocket API. The WebSocket
client is **async-only** and lives behind the `ws` extra:

```shell
pip install "datamaxi[ws]"
```

```python
import asyncio
from datamaxi.aio.ws import AsyncDatamaxiWS


async def main():
    # Reads DATAMAXI_API_KEY from the environment, or pass api_key=... explicitly.
    async with AsyncDatamaxiWS() as ws:
        stream = await ws.ticker.subscribe("BTC-USDT@binance", market="spot")
        async for msg in stream:
            print(msg["s"], msg.get("p"))  # symbol, price


asyncio.run(main())
```

### Channels

Each accessor on `AsyncDatamaxiWS` maps to one channel. `subscribe(*params)` is a
coroutine returning an **async iterator** over live messages; `stream()` (for the
param-less firehose feeds) does the same. Pass the raw param strings shown below —
you can also read the expected shape at runtime via `ws.<channel>.param_format`.

| Accessor                    | Call                                        | Param format                                        | Plan  |
| --------------------------- | ------------------------------------------- | --------------------------------------------------- | ----- |
| `ws.ticker`                 | `subscribe(*p, market="spot"\|"futures")`   | `SYMBOL@exchange[@currency@conversionBase]`         | Basic |
| `ws.forex`                  | `subscribe(*p)`                             | `SYMBOL`                                             | Basic |
| `ws.premium`                | `subscribe(*p)`                             | `src:tgt:tokenId:srcQuote:tgtQuote:srcMkt:tgtMkt`    | Basic |
| `ws.funding_rate`           | `subscribe(*p)`                             | `SYMBOL@exchange`                                    | Basic |
| `ws.open_interest`          | `subscribe(*p)`                             | `SYMBOL@exchange`                                    | Basic |
| `ws.liquidation`            | `subscribe(*p)`                             | `SYMBOL@exchange`                                    | Basic |
| `ws.liquidation_feed`       | `stream()`                                  | — (firehose, no params)                             | Basic |
| `ws.announcement`           | `subscribe()`                               | — (no params)                                       | Pro+  |
| `ws.announcement_internal`  | `subscribe()`                               | — (no params)                                       | Pro+  |

### Multiplexing and filtering

One connection is opened per channel and multiplexes every param you subscribe
to. Because the protocol tags messages by payload fields (not by a subscription
id), `subscribe()` yields **every** message on the channel — filter client-side
by symbol (`msg["s"]`) when you subscribe to more than one:

```python
stream = await ws.ticker.subscribe(
    "BTC-USDT@binance", "ETH-USDT@binance", market="spot"
)
async for msg in stream:
    if msg["s"] == "BTC-USDT":
        handle_btc(msg)
```

Add or drop params on the fly:

```python
await ws.ticker.subscribe("SOL-USDT@binance", market="spot")   # add
await ws.ticker.unsubscribe("SOL-USDT@binance", market="spot") # remove
```

> Not every channel supports removing an individual param server-side —
> `liquidation` and `open_interest` are subscribe-only. Closing the client (see
> [Lifecycle](#lifecycle)) always stops all streams.

### Firehose feeds

`ws.liquidation_feed` needs no subscription — call `stream()` and consume:

```python
async for evt in await ws.liquidation_feed.stream():
    print(evt["s"], evt.get("sd"), evt.get("p"))  # symbol, side, price
```

### Reconnect and keepalive

The client is resilient by default:

- **Auto-reconnect** — if the connection drops it reconnects and replays your
  active subscriptions, so your `async for` loop resumes without extra code.
  Disable with `AsyncDatamaxiWS(reconnect=False)`.
- **Keepalive** — an app-level `PING` is sent every 30s to stay under the
  server's idle timeout. Tune with the `keepalive=<seconds>` argument (`0`
  disables it).

### Lifecycle

Use `AsyncDatamaxiWS` as an async context manager (shown above) so all open
connections close cleanly, or manage it yourself:

```python
ws = AsyncDatamaxiWS()
try:
    async for msg in await ws.forex.subscribe("USD-KRW"):
        ...
finally:
    await ws.aclose()
```

Constructor options: `api_key`, `base_url` (derives the `wss://` URL) or an
explicit `ws_url`, `keepalive`, `reconnect`, and `connect_kwargs` (passed through
to the underlying `websockets.connect`).

### Message shapes

Each message is a plain `dict`. Compact channels use short wire keys (`s` =
symbol, plus per-channel fields like `p`, `e`, `r`, `oi`, …), while others
(`premium`, announcements) use descriptive keys. The exact typed shape of every
channel is generated into
[`datamaxi._ws_models`](https://github.com/bisonai/datamaxi-python/blob/main/datamaxi/_ws_models.py)
as `TypedDict`s, and field meanings are documented in the
[API docs](https://docs.datamaxiplus.com/):

```python
from datamaxi._ws_models import TickerMessage, PremiumMessage
```

> Orderbook streaming is intentionally not exposed.

## Response Types

Most methods return pandas DataFrames by default. Set `pandas=False` to get raw dict/list responses.

```python
# DataFrame response (default)
df = maxi.cex.candle(exchange="binance", symbol="BTC-USDT", interval="1d", market="spot")
print(type(df))  # <class 'pandas.core.frame.DataFrame'>

# Dict response
data = maxi.cex.candle(exchange="binance", symbol="BTC-USDT", interval="1d", market="spot", pandas=False)
print(type(data))  # <class 'dict'>
```

Response metadata (rate-limit headers, etc.) is available on the client after a
call via `maxi.<resource>.last_response`. The older `show_limit_usage` /
`show_header` options that folded metadata into the return value are deprecated
and will be removed in a future major release.

## Pagination

Many endpoints support pagination and return a `next_request` function:

```python
# First page
data, next_request = maxi.cex.announcement(page=1, limit=100)

# Get next page
data2, next_request2 = next_request()

# And so on...
data3, next_request3 = next_request2()
```

On the [async client](#async-client), `next_request` is itself a coroutine —
`await` it: `data2, _ = await next_request()`.

## Error Handling

All SDK exceptions subclass `datamaxi.error.Error`:

| Exception                          | Raised when                                                              |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `ClientError`                      | Server returns a 4xx response. Has `status_code`, `error_message`, `header`, `error_data`. |
| `ServerError`                      | Server returns a 5xx response. Has `status_code`, `message`.             |
| `ParameterRequiredError`           | A required parameter was missing/empty.                                  |
| `AtLeastOneParameterRequiredError` | An endpoint needs at least one of a set of parameters, none given.       |

```python
from datamaxi import Datamaxi
from datamaxi.error import ClientError, ServerError

maxi = Datamaxi()

try:
    df = maxi.cex.candle(exchange="binance", symbol="BTC-USDT", interval="1d", market="spot")
except ClientError as e:
    print(f"Client error {e.status_code}: {e.error_message}")
except ServerError as e:
    print(f"Server error {e.status_code}: {e.message}")
```

## Async Client

`AsyncDatamaxi` is the asynchronous counterpart to `Datamaxi` (built on
[httpx](https://www.python-httpx.org/)). It mirrors the same resource tree and
arguments, with one rule: every method is a coroutine and must be `await`ed.
Install the async extra:

```shell
pip install "datamaxi[async]"
```

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    # Reads DATAMAXI_API_KEY from the environment, or pass api_key=... explicitly.
    async with AsyncDatamaxi() as client:
        df = await client.cex.candle(
            exchange="binance", symbol="BTC-USDT", interval="1d", market="spot"
        )
        print(df.head())


asyncio.run(main())
```

Use `AsyncDatamaxi` as an async context manager (shown above) or call
`await client.aclose()` yourself. Paginated endpoints return an async
`next_request` — `await` it too
(`data, next_request = await client.cex.announcement(...)`). Telegram and Naver
are mounted as `client.telegram` / `client.naver`; standalone
`AsyncTelegram` / `AsyncNaver` clients remain available too.

Every endpoint in the [REST API Reference](#rest-api-reference) works the same
under the async client — see the [docs](https://datamaxi.readthedocs.io/) where
each example has a Sync/Async tab. For real-time streaming, see
[WebSockets](#websockets).

## Local Development

This project uses [uv](https://docs.astral.sh/uv/) for fast dev setup. Install
uv first (see the [uv docs](https://docs.astral.sh/uv/getting-started/installation/)).

```shell
git clone https://github.com/bisonai/datamaxi-python.git
cd datamaxi-python

# Create a virtual environment and install dev dependencies
# (requirements-dev.txt pulls in the test and docs stacks).
uv venv
uv pip install -r requirements/requirements-dev.txt

# For runtime dependencies only:
# uv pip install -r requirements/common.txt
```

Dependency files under `requirements/`:

| File                    | Contents                                                             |
| ----------------------- | ------------------------------------------------------------------- |
| `common.txt`            | Runtime dependencies (`requests`, `pandas`).                        |
| `requirements.txt`      | Alias for `common.txt`.                                             |
| `requirements-test.txt` | `common.txt` + test/lint tooling (pytest, responses, black, flake8). |
| `requirements-dev.txt`  | `requirements-test.txt` + docs tooling (mkdocs).                    |

The `[async]` and `[ws]` extras add `httpx` and `websockets` respectively — the
test stack installs them so the async and WebSocket suites can run.

## Tests

```shell
# Install test dependencies (skip if you already ran the dev install above)
uv pip install -r requirements/requirements-test.txt

# Run keyless tests (no API key required) — this is the lane CI runs on every push
uv run pytest tests/ -m "not integration" -v

# Run integration tests (requires API key)
export DATAMAXI_API_KEY="your_api_key"
uv run pytest tests/test_integration.py -v

# Test specific endpoint groups using markers
uv run pytest tests/test_integration.py -m "cex" -v
uv run pytest tests/test_integration.py -m "funding" -v
uv run pytest tests/test_integration.py -m "premium" -v
uv run pytest tests/test_integration.py -m "forex" -v
uv run pytest tests/test_integration.py -m "telegram" -v
uv run pytest tests/test_integration.py -m "naver" -v
uv run pytest tests/test_integration.py -m "types" -v

# Run all tests
uv run pytest tests/ -v
```

## Links

- [Official Website](https://datamaxiplus.com/)
- [Documentation](https://docs.datamaxiplus.com/)

## Contributing

We welcome contributions!
If you discover a bug in this project, please feel free to open an issue to discuss the changes you would like to propose.

## License

[MIT License](LICENSE)
</content>
