# CEX Wallet Status

Deposit and withdrawal availability for centralized exchange assets.

## Usage

```python
from datamaxi import Datamaxi

maxi = Datamaxi(api_key="YOUR_API_KEY")

exchanges = maxi.cex.wallet_status.exchanges()
assets = maxi.cex.wallet_status.assets(exchange="binance")

status = maxi.cex.wallet_status(exchange="binance", asset="BTC")
```

## Notes

- Set `pandas=False` to return the raw dict response.

::: datamaxi.resources.CexWalletStatus
    options:
      show_submodules: true
      show_source: false
