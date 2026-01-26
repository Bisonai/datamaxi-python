# Premium

Cross-exchange premium data for arbitrage and market dislocation analysis.

## Usage

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

## Notes

- Use `min_`/`max_` filters to narrow price difference, volume, and funding data.
- Set `pandas=False` to return the raw list response.

::: datamaxi.datamaxi.Premium
    options:
      show_submodules: true
      show_source: false
