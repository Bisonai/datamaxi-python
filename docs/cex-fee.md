# CEX Fees

Trading fee schedules for centralized exchanges.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.cex.fee.exchanges()
symbols = maxi.cex.fee.symbols(exchange="binance")

fees = maxi.cex.fee(exchange="binance", symbol="BTC-USDT")
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        exchanges = await client.cex.fee.exchanges()
        symbols = await client.cex.fee.symbols(exchange="binance")

        fees = await client.cex.fee(exchange="binance", symbol="BTC-USDT")


asyncio.run(main())
```

</details>

## Notes

- You can omit `symbol` to get all symbols for the exchange.

::: datamaxi.resources.CexFee
    options:
      show_submodules: true
      show_source: false
