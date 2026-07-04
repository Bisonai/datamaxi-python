# CEX Ticker

Real-time ticker snapshots for centralized exchanges.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.cex.ticker.exchanges(market="spot")
symbols = maxi.cex.ticker.symbols(exchange="binance", market="spot")

ticker = maxi.cex.ticker.get(
    exchange="binance",
    symbol="BTC-USDT",
    market="spot",
    currency="USD",
)
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        exchanges = await client.cex.ticker.exchanges(market="spot")
        symbols = await client.cex.ticker.symbols(exchange="binance", market="spot")

        ticker = await client.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
            currency="USD",
        )


asyncio.run(main())
```

</details>

## Notes

- Use `conversion_base` when you need cross-currency conversions.
- Set `pandas=False` to return the raw dict response.

::: datamaxi.resources.CexTicker
    options:
      show_submodules: true
      show_source: false
