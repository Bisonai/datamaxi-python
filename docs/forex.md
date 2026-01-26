# Forex

Foreign exchange spot rates.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

symbols = maxi.forex.symbols()
data = maxi.forex(symbol="USD-KRW")
```

## Notes

- Set `pandas=False` to return the raw dict response.

::: datamaxi.datamaxi.Forex
    options:
      show_submodules: true
      show_source: false
