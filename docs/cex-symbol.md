# CEX Symbol

Per-base / per-symbol CEX metadata and aggregates: trading status, tags, cautions, delistings, volume, Open Interest, and liquidation.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

# Trading status + caution + tags + delisting metadata
metadata = maxi.cex.symbol.metadata(exchange="binance", base="BTC")

# Exchange-assigned tags (e.g. seed, alpha)
tags = maxi.cex.symbol.tags(exchange="binance", base="BTC")

# Active caution / investment-warning flags
cautions = maxi.cex.symbol.cautions(exchange="binance")

# Scheduled delistings with timestamps
delistings = maxi.cex.symbol.delistings(exchange="binance")

# Per-exchange 24h volume for a single base asset
volume = maxi.cex.symbol.volume(base="BTC")

# Per-exchange Open Interest for a single base asset
oi = maxi.cex.symbol.oi(base="BTC", exchange="binance")

# Per-exchange OI snapshot with 1h / 4h / 24h deltas
oi_stats = maxi.cex.symbol.oi_stats(base="BTC", exchange="binance", currency="USD")

# Per-exchange long / short liquidation aggregates over a window
liquidation = maxi.cex.symbol.liquidation(base="BTC", window="24h")
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        # Trading status + caution + tags + delisting metadata
        metadata = await client.cex.symbol.metadata(exchange="binance", base="BTC")

        # Exchange-assigned tags (e.g. seed, alpha)
        tags = await client.cex.symbol.tags(exchange="binance", base="BTC")

        # Active caution / investment-warning flags
        cautions = await client.cex.symbol.cautions(exchange="binance")

        # Scheduled delistings with timestamps
        delistings = await client.cex.symbol.delistings(exchange="binance")

        # Per-exchange 24h volume for a single base asset
        volume = await client.cex.symbol.volume(base="BTC")

        # Per-exchange Open Interest for a single base asset
        oi = await client.cex.symbol.oi(base="BTC", exchange="binance")

        # Per-exchange OI snapshot with 1h / 4h / 24h deltas
        oi_stats = await client.cex.symbol.oi_stats(base="BTC", exchange="binance", currency="USD")

        # Per-exchange long / short liquidation aggregates over a window
        liquidation = await client.cex.symbol.liquidation(base="BTC", window="24h")


asyncio.run(main())
```

</details>

## Notes

- `metadata` and `tags` take optional `exchange` / `base` filters; `cautions` and `delistings` filter by `exchange` (and `market`). Omit filters to fetch across all symbols.
- `oi_stats` accepts `currency` of `USD` or `KRW`.

::: datamaxi.resources.CexSymbol
    options:
      show_submodules: true
      show_source: false
