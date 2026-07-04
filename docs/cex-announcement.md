# CEX Announcement

Exchange announcements such as listings and delistings.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

data, next_request = maxi.cex.announcement(
    exchange="binance",
    category="listing",
    page=1,
    limit=50,
    sort="desc",
)

more_data, _ = next_request()
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        data, next_request = await client.cex.announcement(
            exchange="binance",
            category="listing",
            page=1,
            limit=50,
            sort="desc",
        )

        more_data, _ = await next_request()


asyncio.run(main())
```

</details>

## Notes

- Pagination returns a `next_request` function for the next page.

::: datamaxi.resources.CexAnnouncement
    options:
      show_submodules: true
      show_source: false
