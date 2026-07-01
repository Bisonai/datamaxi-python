# Index Price

Historical index price time series for a single asset.

## Usage

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

## Notes

- `from_` is spelled with a trailing underscore because `from` is a Python
  keyword; the wire-level query param remains `from`.

::: datamaxi.datamaxi.IndexPrice
    options:
      show_submodules: true
      show_source: false
