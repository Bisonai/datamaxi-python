# CEX Announcement

Exchange announcements such as listings and delistings.

## Usage

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

## Notes

- Pagination returns a `next_request` function for the next page.

::: datamaxi.datamaxi.CexAnnouncement
    options:
      show_submodules: true
      show_source: false
