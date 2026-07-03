# CEX Fees

Trading fee schedules for centralized exchanges.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.cex.fee.exchanges()
symbols = maxi.cex.fee.symbols(exchange="binance")

fees = maxi.cex.fee(exchange="binance", symbol="BTC-USDT")
```

## Notes

- You can omit `symbol` to get all symbols for the exchange.

::: datamaxi.resources.CexFee
    options:
      show_submodules: true
      show_source: false
