# Naver Trend

Search trend data for South Korea via Naver.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

naver = Datamaxi(api_key="YOUR_API_KEY").naver

symbols = naver.symbols()
trend = naver.trend(symbol="BTC")
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        symbols = await client.naver.symbols()
        trend = await client.naver.trend(symbol="BTC")


asyncio.run(main())
```

</details>

## Notes

- Set `pandas=False` to return the raw list response.

::: datamaxi.naver
    options:
      show_submodules: true
      show_source: false
