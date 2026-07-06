# Async client

The SDK ships an async client, `AsyncDatamaxi`, built on
[httpx](https://www.python-httpx.org/). It mirrors the sync
[`Datamaxi`](api.md) resource tree — the same endpoints and arguments — with one
rule: every method is a coroutine and must be `await`ed.

Every endpoint page in this documentation carries a **Sync** / **Async** tab —
switch to the *Async* tab to see the awaited twin of that page's example.

## Installation

The async client requires the `async` extra, which pulls in `httpx`:

```shell
pip install "datamaxi[async]"
```

## Lifecycle

Use `AsyncDatamaxi` as an async context manager so the underlying `httpx` client
is closed cleanly, or call `await client.aclose()` yourself. It reads the same
`DATAMAXI_API_KEY` environment variable as the sync client.

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    # Reads DATAMAXI_API_KEY from the environment, or pass api_key=... explicitly.
    async with AsyncDatamaxi() as client:
        df = await client.cex.candle(
            exchange="binance", symbol="BTC-USDT", interval="1d", market="spot"
        )
        print(df.head())


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

- Every data and discovery method is a coroutine — `await` it (e.g.
  `await client.cex.candle.exchanges(market="spot")`).
- Telegram and Naver are reached via `client.telegram` and `client.naver`. See
  the [Telegram](telegram.md) and [Naver Trend](naver-trend.md) pages for tabbed
  examples.

## Pagination

Paginated endpoints return an **async** `next_request` callable — `await` it too:

```python
data, next_request = await client.cex.announcement(page=1, limit=100)
data2, _ = await next_request()
```

## Reference

::: datamaxi.aio.AsyncDatamaxi
    options:
      show_submodules: false
      show_source: false
