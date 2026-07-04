# Forex

Foreign exchange spot rates.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

symbols = maxi.forex.symbols()
data = maxi.forex(symbol="USD-KRW")
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        symbols = await client.forex.symbols()
        data = await client.forex(symbol="USD-KRW")


asyncio.run(main())
```

</details>

## Notes

- Set `pandas=False` to return the raw dict response.

::: datamaxi.resources.Forex
    options:
      show_submodules: true
      show_source: false
