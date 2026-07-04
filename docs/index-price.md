# Index Price

Historical index price time series for a single asset.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

data = maxi.index_price(
    asset="BTC",
    from_="now - 1 month",
    to="now",
    interval="5m",
)
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        data = await client.index_price(
            asset="BTC",
            from_="now - 1 month",
            to="now",
            interval="5m",
        )


asyncio.run(main())
```

</details>

## Notes

- `from_` is spelled with a trailing underscore because `from` is a Python
  keyword; the wire-level query param remains `from`.

::: datamaxi.resources.IndexPrice
    options:
      show_submodules: true
      show_source: false
