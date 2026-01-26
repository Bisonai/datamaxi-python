# CEX Candle

Historical OHLCV candle data for centralized exchanges.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.cex.candle.exchanges(market="spot")
symbols = maxi.cex.candle.symbols(exchange="binance", market="spot")
intervals = maxi.cex.candle.intervals()

df = maxi.cex.candle(
    exchange="binance",
    symbol="BTC-USDT",
    interval="1d",
    market="spot",
    from_unix=1704067200,
    to_unix=1706745600,
)
```

## Notes

- `from_unix` and `to_unix` use Unix timestamps in seconds.
- Set `pandas=False` to return the raw dict response.

::: datamaxi.datamaxi.CexCandle
    options:
      show_submodules: true
      show_source: false
