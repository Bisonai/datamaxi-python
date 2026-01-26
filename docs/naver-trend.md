# Naver Trend

Search trend data for South Korea via Naver.

## Usage

```python
from datamaxi import Naver

naver = Naver(api_key="YOUR_API_KEY")

symbols = naver.symbols()
trend = naver.trend(symbol="BTC")
```

## Notes

- Set `pandas=False` to return the raw list response.

::: datamaxi.naver
    options:
      show_submodules: true
      show_source: false
