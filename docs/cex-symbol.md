# CEX Symbol

Per-base / per-symbol CEX metadata and aggregates: trading status, tags, cautions, delistings, volume, Open Interest, and liquidation.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

# Trading status + caution + tags + delisting metadata
metadata = maxi.cex.symbol.metadata(exchange="binance", base="BTC")

# Exchange-assigned tags (e.g. seed, alpha)
tags = maxi.cex.symbol.tags(exchange="binance", base="BTC")

# Active caution / investment-warning flags
cautions = maxi.cex.symbol.cautions(exchange="binance", base="BTC")

# Scheduled delistings with timestamps
delistings = maxi.cex.symbol.delistings(exchange="binance", base="BTC")

# Per-exchange 24h volume for a single base asset
volume = maxi.cex.symbol.volume(base="BTC", exchange="binance")

# Per-exchange Open Interest for a single base asset
oi = maxi.cex.symbol.oi(base="BTC", exchange="binance")

# Per-exchange OI snapshot with 1h / 4h / 24h deltas
oi_stats = maxi.cex.symbol.oi_stats(base="BTC", exchange="binance", currency="USD")

# Per-exchange long / short liquidation aggregates over a window
liquidation = maxi.cex.symbol.liquidation(base="BTC", window="24h")
```

## Notes

- `metadata`, `tags`, `cautions`, and `delistings` take optional `exchange` / `base` filters; omit both to fetch across all symbols.
- `oi_stats` accepts `currency` of `USD` or `KRW`.

::: datamaxi.datamaxi.CexSymbol
    options:
      show_submodules: true
      show_source: false
