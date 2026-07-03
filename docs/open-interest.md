# Open Interest

CEX futures Open Interest: latest snapshots, reporting pairs, the token x exchange matrix, top-line aggregates, and aggregated history.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

# Latest OI snapshot for a single futures symbol
snapshot = maxi.open_interest(exchange="binance", symbol="BTC-USDT")

# List all (exchange, symbol) pairs currently reporting OI
pairs = maxi.open_interest.list(exchange="binance")

# Paginated token x exchange OI matrix
overview = maxi.open_interest.overview(
    page=1,
    limit=20,
    key="binance",
    sort="desc",
)

# Top-line OI aggregates (total USD, top tokens, top exchanges)
summary = maxi.open_interest.summary(topN=10)

# Per-exchange aggregated OI history for a single token
history = maxi.open_interest.history_aggregated(
    token_id="bitcoin",
    interval="1h",
)
```

## Notes

- `overview` requires `sort` to be `asc` or `desc`; `summary` accepts `topN` between 1 and 30.
- `history_aggregated` uses the token id (e.g. `bitcoin`), not a ticker, and accepts `interval` of `5m`, `15m`, `1h`, `4h`, or `1d`. Pass `from_` / `to` as unix-ms (`from_` maps to the wire param `from`).

::: datamaxi.resources.OpenInterest
    options:
      show_submodules: true
      show_source: false
