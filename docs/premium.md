# Premium

Cross-exchange premium data for arbitrage and market dislocation analysis.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.premium.exchanges()

data = maxi.premium(
    source_exchange="binance",
    target_exchange="upbit",
    asset="BTC",
    source_market="spot",
    target_market="spot",
    sort="desc",
    key="pdp",
    limit=100,
)
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        exchanges = await client.premium.exchanges()

        data = await client.premium(
            source_exchange="binance",
            target_exchange="upbit",
            asset="BTC",
            source_market="spot",
            target_market="spot",
            sort="desc",
            key="pdp",
            limit=100,
        )


asyncio.run(main())
```

</details>

## Notes

- Use `min_`/`max_` filters to narrow price difference, volume, and funding data.
- Set `pandas=False` to return the raw list response.

::: datamaxi.resources.Premium
    options:
      show_submodules: true
      show_source: false
