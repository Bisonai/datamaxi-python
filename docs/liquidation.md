# Liquidation

CEX futures liquidation data: recent events, firehose feed, heatmaps, maps, and bucketed history.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

# Recent liquidation events for a single futures symbol
events = maxi.liquidation(exchange="binance", symbol="BTC-USDT", limit=100)

# Firehose: most recent events across every symbol
feed = maxi.liquidation.feed(limit=100)

# Token x exchange liquidation heatmap over a rolling window
heatmap = maxi.liquidation.heatmap(window="1h", topN=10)

# Liquidation KPI stats over a rolling window
stats = maxi.liquidation.stats(window="1h")

# Coinglass-style liquidation map (price x leverage tier)
liq_map = maxi.liquidation.map(base="BTC", exchange="binance", quote="USDT")

# Bucketed long / short liquidation USD time series + price line
history = maxi.liquidation.symbol_history(
    symbol="BTC",
    quote="USDT",
    exchange="binance",
    interval="5m",
    window="24h",
)
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        # Recent liquidation events for a single futures symbol
        events = await client.liquidation(exchange="binance", symbol="BTC-USDT", limit=100)

        # Firehose: most recent events across every symbol
        feed = await client.liquidation.feed(limit=100)

        # Token x exchange liquidation heatmap over a rolling window
        heatmap = await client.liquidation.heatmap(window="1h", topN=10)

        # Liquidation KPI stats over a rolling window
        stats = await client.liquidation.stats(window="1h")

        # Coinglass-style liquidation map (price x leverage tier)
        liq_map = await client.liquidation.map(base="BTC", exchange="binance", quote="USDT")

        # Bucketed long / short liquidation USD time series + price line
        history = await client.liquidation.symbol_history(
            symbol="BTC",
            quote="USDT",
            exchange="binance",
            interval="5m",
            window="24h",
        )


asyncio.run(main())
```

</details>

## Notes

- `heatmap` and `stats` accept `window` of `1h`, `4h`, or `24h`; `heatmap`'s `topN` must be between 1 and 30.
- `symbol_history` accepts `interval` of `5m`, `15m`, or `1h` and `window` of `24h`, `72h`, or `7d`.

::: datamaxi.resources.Liquidation
    options:
      show_submodules: true
      show_source: false
