# Async Client

For `asyncio` applications the SDK ships an async client, `AsyncDatamaxi`, built
on [httpx](https://www.python-httpx.org/). It mirrors the sync
[`Datamaxi`](api.md) resource tree — the same endpoints and arguments — but every
request method is a coroutine and must be `await`ed.

## Installation

The async client requires the `async` extra, which pulls in `httpx`:

```shell
pip install "datamaxi[async]"
```

## Usage

Use `AsyncDatamaxi` as an async context manager so the underlying HTTP client is
closed cleanly (or call `await client.aclose()` yourself). It reads the same
`DATAMAXI_API_KEY` environment variable as the sync client.

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    # Reads DATAMAXI_API_KEY from the environment, or pass api_key=... explicitly.
    async with AsyncDatamaxi() as client:
        df = await client.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
        )
        print(df.head())

        ticker = await client.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
        )
        print(ticker)

        premium = await client.premium(asset="BTC")
        print(premium.head())


asyncio.run(main())
```

Without a context manager, close the client explicitly:

```python
client = AsyncDatamaxi()
try:
    df = await client.cex.candle(
        exchange="binance", symbol="BTC-USDT", interval="1d", market="spot"
    )
finally:
    await client.aclose()
```

## Notes

- Every data method is a coroutine — `await` it (e.g. `await client.cex.candle(...)`).
- `AsyncDatamaxi` mirrors the sync resource tree: `cex.*` (candle, ticker, fee,
  `wallet_status`, announcement, token, symbol), `funding_rate`, `forex`,
  `premium`, `liquidation`, `open_interest`, `margin_borrow`, and `index_price`.
- Paginated endpoints return an **async** `next_request` callable — `await` it too:

```python
data, next_request = await client.cex.announcement(page=1, limit=100)
data2, next_request2 = await next_request()
```

- Telegram and Naver have standalone async clients, `AsyncTelegram` and
  `AsyncNaver` (also async context managers):

```python
from datamaxi.aio import AsyncTelegram, AsyncNaver

async with AsyncTelegram() as telegram:
    channels, next_request = await telegram.channels(page=1, limit=100)

async with AsyncNaver() as naver:
    trend = await naver.trend(symbol="BTC")
```

## Reference

::: datamaxi.aio.AsyncDatamaxi
    options:
      show_submodules: false
      show_source: false
