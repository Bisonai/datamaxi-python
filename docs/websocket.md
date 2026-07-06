# WebSocket

Stream real-time market data over the DataMaxi+ WebSocket API. Unlike the REST
resources, the WebSocket client is **async-only** — there is no synchronous
variant.

## Installation

The WebSocket client requires the `ws` extra, which pulls in
[`websockets`](https://websockets.readthedocs.io/):

```shell
pip install "datamaxi[ws]"
```

## Quickstart

`AsyncDatamaxiWS` reads the same `DATAMAXI_API_KEY` environment variable as the
REST clients (or pass `api_key=...`). Use it as an async context manager so open
connections close cleanly.

```python
import asyncio
from datamaxi.aio.ws import AsyncDatamaxiWS


async def main():
    async with AsyncDatamaxiWS() as ws:
        stream = await ws.ticker.subscribe("BTC-USDT@binance", market="spot")
        async for msg in stream:
            print(msg["s"], msg.get("p"))  # symbol, price


asyncio.run(main())
```

`subscribe(*params)` is a coroutine that returns an **async iterator** over live
messages. Iterate it with `async for`.

## Channels

Each accessor on `AsyncDatamaxiWS` maps to one channel. Pass the raw param
strings shown below; you can also inspect the expected format at runtime via
`ws.<channel>.param_format`.

| Accessor                    | Call                                        | Param format                                        | Plan  |
| --------------------------- | ------------------------------------------- | --------------------------------------------------- | ----- |
| `ws.ticker`                 | `subscribe(*p, market="spot"\|"futures")`   | `SYMBOL@exchange[@currency@conversionBase]`         | Basic |
| `ws.forex`                  | `subscribe(*p)`                             | `SYMBOL`                                             | Basic |
| `ws.premium`                | `subscribe(*p)`                             | `src:tgt:tokenId:srcQuote:tgtQuote:srcMkt:tgtMkt`    | Basic |
| `ws.funding_rate`           | `subscribe(*p)`                             | `SYMBOL@exchange`                                    | Basic |
| `ws.open_interest`          | `subscribe(*p)`                             | `SYMBOL@exchange`                                    | Basic |
| `ws.liquidation`            | `subscribe(*p)`                             | `SYMBOL@exchange`                                    | Basic |
| `ws.liquidation_feed`       | `stream()`                                  | — (firehose, no params)                             | Basic |
| `ws.announcement`           | `subscribe()`                               | — (no params)                                       | Pro+  |
| `ws.announcement_internal`  | `subscribe()`                               | — (no params)                                       | Pro+  |

`ticker` is market-keyed — pass `market="spot"` (default) or `market="futures"`.
The announcement channels require a **Pro+** plan.

## Multiplexing and filtering

One connection is opened per channel and multiplexes every param you subscribe
to. Because the protocol tags messages by payload fields (not by a subscription
id), `subscribe()` yields **every** message on the channel — filter client-side
by symbol (`msg["s"]`) when subscribing to more than one:

```python
stream = await ws.ticker.subscribe(
    "BTC-USDT@binance", "ETH-USDT@binance", market="spot"
)
async for msg in stream:
    if msg["s"] == "BTC-USDT":
        handle_btc(msg)
```

Add or drop params on the fly:

```python
await ws.ticker.subscribe("SOL-USDT@binance", market="spot")   # add
await ws.ticker.unsubscribe("SOL-USDT@binance", market="spot") # remove
```

> Not every channel supports removing an individual param server-side —
> `liquidation` and `open_interest` are subscribe-only. Closing the client
> (`await ws.aclose()`, or exiting the `async with` block) always stops all
> streams.

## Firehose feeds

`ws.liquidation_feed` needs no subscription — call `stream()` and consume:

```python
async for evt in await ws.liquidation_feed.stream():
    print(evt["s"], evt.get("sd"), evt.get("p"))  # symbol, side, price
```

## Reconnect and keepalive

The client is resilient by default:

- **Auto-reconnect** — if the connection drops it reconnects and replays your
  active subscriptions, so your `async for` loop resumes without extra code.
  Disable with `AsyncDatamaxiWS(reconnect=False)`.
- **Keepalive** — an app-level `PING` is sent every 30 seconds to stay under the
  server's idle timeout. Tune it with the `keepalive=<seconds>` argument (`0`
  disables it).

## Lifecycle

Use `AsyncDatamaxiWS` as an async context manager, or manage it yourself:

```python
ws = AsyncDatamaxiWS()
try:
    async for msg in await ws.forex.subscribe("USD-KRW"):
        ...
finally:
    await ws.aclose()
```

Constructor options: `api_key`, `base_url` (derives the `wss://` URL) or an
explicit `ws_url`, `keepalive`, `reconnect`, and `connect_kwargs` (passed through
to the underlying `websockets.connect`).

## Message shapes

Each message is a plain `dict`. Compact channels use short wire keys (`s` =
symbol, plus per-channel fields like `p`, `e`, `r`, `oi`, …), while others
(`premium`, announcements) use descriptive keys. The typed shape of every channel
is generated into `datamaxi._ws_models` as `TypedDict`s, and field meanings are
documented in the [API docs](https://docs.datamaxiplus.com/):

```python
from datamaxi._ws_models import TickerMessage, PremiumMessage
```

Orderbook streaming is intentionally not exposed.

## Reference

::: datamaxi.aio.ws.AsyncDatamaxiWS
    options:
      show_submodules: false
      show_source: false
</content>
