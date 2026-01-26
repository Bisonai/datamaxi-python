# Funding Rate

Historical and latest funding rates for perpetual futures.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.funding_rate.exchanges()
symbols = maxi.funding_rate.symbols(exchange="binance", market="futures")

history, next_request = maxi.funding_rate.history(
    exchange="binance",
    symbol="BTC-USDT",
    page=1,
    limit=100,
    sort="desc",
)

latest = maxi.funding_rate.latest(exchange="binance", symbol="BTC-USDT")
```

## Notes

- Pagination returns a `next_request` function for the next page.
- Set `pandas=False` to return the raw dict response.

::: datamaxi.datamaxi.FundingRate
    options:
      show_submodules: true
      show_source: false
