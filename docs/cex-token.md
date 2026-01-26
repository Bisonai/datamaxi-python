# CEX Token

Token listing and delisting updates from centralized exchanges.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

data, next_request = maxi.cex.token.updates(
    type="listed",
    page=1,
    limit=100,
    sort="desc",
)

more_data, _ = next_request()
```

## Notes

- Use `type="listed"` or `type="delisted"` to filter update types.

::: datamaxi.datamaxi.CexToken
    options:
      show_submodules: true
      show_source: false
