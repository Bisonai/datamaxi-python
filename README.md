# DataMaxi+ Python SDK

[![PyPI version](https://img.shields.io/pypi/v/datamaxi)](https://pypi.python.org/pypi/datamaxi)
[![Python version](https://img.shields.io/pypi/pyversions/datamaxi)](https://www.python.org/downloads/)
[![Documentation](https://img.shields.io/badge/docs-latest-blue)](https://datamaxi.readthedocs.io/en/stable/)
[![Code Style](https://img.shields.io/badge/code_style-black-black)](https://black.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the official implementation of Python SDK for DataMaxi+ API.
The package can be used to fetch both historical and latest data using [DataMaxi+ API](https://docs.datamaxiplus.com/).
This package is compatible with Python v3.8+.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Quickstart](#quickstart)
- [API Reference](#api-reference)
  - [CEX Candle Data](#cex-candle-data)
  - [CEX Ticker Data](#cex-ticker-data)
  - [CEX Trading Fees](#cex-trading-fees)
  - [CEX Wallet Status](#cex-wallet-status)
  - [CEX Announcements](#cex-announcements)
  - [CEX Token Updates](#cex-token-updates)
  - [DEX Data](#dex-data)
  - [Funding Rate](#funding-rate)
  - [Premium](#premium)
  - [Forex](#forex)
  - [Telegram](#telegram)
  - [Naver Trend](#naver-trend)
- [Response Types](#response-types)
- [Pagination](#pagination)
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

- `Datamaxi` - Main client for crypto trading data (CEX, DEX, funding rates, premium, forex)
- `Telegram` - Client for Telegram channel data
- `Naver` - Client for Naver trend data

```python
from datamaxi import Datamaxi, Telegram, Naver

# Initialize clients
api_key = "your_api_key"
maxi = Datamaxi(api_key=api_key)
telegram = Telegram(api_key=api_key)
naver = Naver(api_key=api_key)

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

## API Reference

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
    sort="desc"              # Optional: "asc" or "desc"
)
```

### DEX Data

Fetch data from decentralized exchanges. (Experimental)

```python
# Get supported chains
chains = maxi.dex.chains()

# Get supported exchanges
exchanges = maxi.dex.exchanges()

# Get supported pools
pools = maxi.dex.pools(exchange="klayswap", chain="kaia_mainnet")

# Get supported intervals
intervals = maxi.dex.intervals()

# Fetch trade data
df, next_request = maxi.dex.trade(
    chain="bsc_mainnet",                              # Required: blockchain
    exchange="pancakeswap",                           # Required: DEX name
    pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",  # Required: pool address
    fromDateTime=None,       # Optional: start datetime (format: "2006-01-02" or "2006-01-02 15:04:05")
    toDateTime=None,         # Optional: end datetime
    page=1,                  # Optional: page number
    limit=1000,              # Optional: items per page
    sort="desc",             # Optional: "asc" or "desc"
    pandas=True              # Optional: return DataFrame or dict
)

# Fetch candle data
df, next_request = maxi.dex.candle(
    chain="bsc_mainnet",
    exchange="pancakeswap",
    pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
    interval="1d",           # Optional: candle interval (default: 1d)
    fromDateTime=None,
    toDateTime=None,
    page=1,
    limit=1000,
    sort="desc",
    pandas=True
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

# Fetch premium data with filtering
df = maxi.premium(
    source_exchange=None,    # Optional: source exchange
    target_exchange=None,    # Optional: target exchange
    asset=None,              # Optional: asset symbol (e.g., "BTC")
    source_quote=None,       # Optional: source quote currency
    target_quote=None,       # Optional: target quote currency
    source_market=None,      # Optional: "spot" or "futures"
    target_market=None,      # Optional: "spot" or "futures"
    page=1,                  # Optional: page number
    limit=100,               # Optional: items per page
    sort=None,               # Optional: "asc" or "desc"
    key=None,                # Optional: sort key (e.g., "pdp")
    currency=None,           # Optional: price currency
    conversion_base=None,    # Optional: conversion base

    # Price difference filters
    min_pd=None,             # Optional: min price difference (USD)
    max_pd=None,             # Optional: max price difference (USD)
    min_pdp=None,            # Optional: min price difference percentage
    max_pdp=None,            # Optional: max price difference percentage
    min_pdp24h=None,         # Optional: min 24h price difference %
    max_pdp24h=None,         # Optional: max 24h price difference %
    # ... and more time-based filters (pdp4h, pdp1h, pdp30m, pdp15m, pdp5m)

    # Volume filters
    min_sv=None,             # Optional: min source 24h volume
    max_sv=None,             # Optional: max source 24h volume
    min_tv=None,             # Optional: min target 24h volume
    max_tv=None,             # Optional: max target 24h volume

    # Funding rate filters
    min_net_funding_rate=None,
    max_net_funding_rate=None,
    min_source_funding_rate=None,
    max_source_funding_rate=None,
    min_target_funding_rate=None,
    max_target_funding_rate=None,

    # Other filters
    only_transferable=False, # Optional: filter by transferable assets
    network=None,            # Optional: filter by network
    source_funding_rate_interval=None,
    target_funding_rate_interval=None,
    premium_type=None,       # Optional: premium type
    token_include=None,      # Optional: include specific tokens
    token_exclude=None,      # Optional: exclude specific tokens

    pandas=True              # Optional: return DataFrame or dict
)
```

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

## Local Development

```shell
git clone https://github.com/bisonai/datamaxi-python.git
cd datamaxi-python
pip install -r requirements/common.txt
```

## Tests

```shell
# Install test dependencies
pip install -r requirements/requirements-test.txt

# Run unit tests (no API key required)
python -m pytest tests/test_api.py -v

# Run integration tests (requires API key)
export DATAMAXI_API_KEY="your_api_key"
python -m pytest tests/test_integration.py -v

# Test specific endpoint groups using markers
python -m pytest tests/test_integration.py -m "cex" -v
python -m pytest tests/test_integration.py -m "dex" -v
python -m pytest tests/test_integration.py -m "funding" -v
python -m pytest tests/test_integration.py -m "premium" -v
python -m pytest tests/test_integration.py -m "forex" -v
python -m pytest tests/test_integration.py -m "telegram" -v
python -m pytest tests/test_integration.py -m "naver" -v

# Run all tests
python -m pytest tests/ -v
```

## Links

- [Official Website](https://datamaxiplus.com/)
- [Documentation](https://docs.datamaxiplus.com/)

## Contributing

We welcome contributions!
If you discover a bug in this project, please feel free to open an issue to discuss the changes you would like to propose.

## License

[MIT License](license.md)
