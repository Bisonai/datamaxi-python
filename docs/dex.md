# DEX

Decentralized exchange trade and candle data. These endpoints are experimental.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

chains = maxi.dex.chains()
exchanges = maxi.dex.exchanges()
pools = maxi.dex.pools(exchange="pancakeswap", chain="bsc_mainnet")
intervals = maxi.dex.intervals()

trades, next_request = maxi.dex.trade(
    chain="bsc_mainnet",
    exchange="pancakeswap",
    pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
    fromDateTime="2024-01-01",
    page=1,
    limit=100,
)

candles, _ = maxi.dex.candle(
    chain="bsc_mainnet",
    exchange="pancakeswap",
    pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
    interval="1d",
)
```

## Notes

- `fromDateTime` and `toDateTime` are mutually exclusive.
- Pagination returns a `next_request` function for the next page.

::: datamaxi.datamaxi.Dex
    options:
      show_submodules: true
      show_source: false
