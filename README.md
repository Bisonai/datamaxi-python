# DataMaxi+ Python SDK

[![PyPI version](https://img.shields.io/pypi/v/datamaxi)](https://pypi.python.org/pypi/datamaxi)
[![Python version](https://img.shields.io/pypi/pyversions/datamaxi)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://datamaxi.readthedocs.io/en/stable/)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [DataMaxi+ API](https://docs.datamaxiplus.com/).
Fetch both historical and latest market data across centralized exchanges (OHLCV
candles, tickers, trading fees, wallet status, announcements), perpetual funding
rates, cross-exchange price premiums for arbitrage, forex rates, Telegram channel
data, and Naver search trends.

This package is compatible with Python v3.10+.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Quickstart](#quickstart)
- [Async Client](#async-client)
- [API Reference](#api-reference)
  - [CEX Candle Data](#cex-candle-data)
  - [CEX Ticker Data](#cex-ticker-data)
  - [CEX Trading Fees](#cex-trading-fees)
  - [CEX Wallet Status](#cex-wallet-status)
  - [CEX Announcements](#cex-announcements)
  - [CEX Token Updates](#cex-token-updates)
  - [Funding Rate](#funding-rate)
  - [Premium](#premium)
  - [Forex](#forex)
  - [Telegram](#telegram)
  - [Naver Trend](#naver-trend)
- [Response Types](#response-types)
- [Pagination](#pagination)
- [Error Handling](#error-handling)
- [Local Development](#local-development)
- [Tests](#tests)
- [Links](#links)
- [Contributing](#contributing)
- [License](#license)

## Installation

```shell
pip install datamaxi
```

## Configuration

Private API endpoints are protected by an API key.
You can get the API key upon registering at https://datamaxiplus.com/auth.

| Option             | Explanation                                                                           |
|--------------------|---------------------------------------------------------------------------------------|
| `api_key`          | Your API key                                                                          |
| `base_url`         | If `base_url` is not provided, it defaults to `https://api.datamaxiplus.com`.         |
| `timeout`          | Number of seconds to wait for a server response. By default requests do not time out. |
| `proxies`          | Proxy through which the request is queried                                            |
| `show_limit_usage` | Return response as dictionary including `"limit_usage"` and `"data"` keys             |
| `show_header`      | Return response as dictionary including `"header"` and `"data"` keys                  |

### Environment Variables

You may use environment variables to configure the SDK to avoid any inline boilerplate.

| Env                | Description                                  |
| ------------------ | -------------------------------------------- |
| `DATAMAXI_API_KEY` | Used instead of `api_key` if none is passed. |

## Quickstart

DataMaxi+ Python package includes the following clients:

- `Datamaxi` - Main (synchronous) client for crypto trading data (CEX, funding rates, premium, forex)
- `Telegram` - Client for Telegram channel data
- `Naver` - Client for Naver trend data

An asynchronous variant, `AsyncDatamaxi`, is covered in [Async Client](#async-client).

Set your API key via the `DATAMAXI_API_KEY` environment variable (recommended, so
the key stays out of source code):

```shell
export DATAMAXI_API_KEY="your_api_key"
```

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi, Telegram, Naver

# Clients read DATAMAXI_API_KEY from the environment automatically.
# Alternatively, pass api_key="your_api_key" explicitly to each client.
maxi = Datamaxi()
telegram = Telegram()
naver = Naver()

# Fetch CEX candle data (returns pandas DataFrame)
df = maxi.cex.candle(
    exchange="binance",
    symbol="BTC-USDT",
    interval="1d",
    market="spot"
)
print(df.head())

# Fetch ticker data
ticker = maxi.cex.ticker.get(
    exchange="binance",
    symbol="BTC-USDT",
    market="spot"
)
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
        # Fetch CEX candle data (returns pandas DataFrame)
        df = await client.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
        )
        print(df.head())

        # Fetch ticker data
        ticker = await client.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
        )
        print(ticker)

        # Fetch premium data
        premium = await client.premium(asset="BTC")
        print(premium.head())


asyncio.run(main())
```

</details>

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
have standalone `AsyncTelegram` / `AsyncNaver` clients.

Every endpoint in the [API Reference](#api-reference) works the same under the
async client — see the [docs](https://datamaxi.readthedocs.io/) where each
example has a Sync/Async tab.

## API Reference

> **Discovery helpers.** Most endpoints expose helpers to list valid argument
> values before you fetch — commonly `.exchanges()`, `.symbols(exchange=...)`, and
> (for candles) `.intervals()`. Use them to discover supported exchanges, trading
> pairs, and intervals. The examples below show them per endpoint.

### CEX Candle Data

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

### CEX Ticker Data

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

### CEX Trading Fees

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

### CEX Wallet Status

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

### CEX Announcements

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

### CEX Token Updates

Fetch token listing/delisting updates.

```python
# Fetch token updates
data, next_request = maxi.cex.token.updates(
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    type=None,               # Optional: "listed" or "delisted"
)
```

### Funding Rate

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

### Premium

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

### Forex

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

### Telegram

Fetch Telegram channel messages and metadata.

```python
# Initialize Telegram client
from datamaxi import Telegram
telegram = Telegram(api_key=api_key)

# Fetch channels
data, next_request = telegram.channels(
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    category=None,           # Optional: filter by category
    key=None,                # Optional: sort key
    sort="desc"              # Optional: "asc" or "desc"
)

# Fetch messages
data, next_request = telegram.messages(
    channel_name=None,       # Optional: filter by channel
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    key=None,                # Optional: sort key
    sort="desc",             # Optional: "asc" or "desc"
    category=None            # Optional: filter by category
)
```

### Naver Trend

Fetch Naver search trend data (South Korea).

```python
# Initialize Naver client
from datamaxi import Naver
naver = Naver(api_key=api_key)

# Get supported symbols
symbols = naver.symbols()

# Fetch trend data
data = naver.trend(
    symbol="BTC",            # Required: symbol to search
    pandas=True              # Optional: return DataFrame or list
)
```

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
