"""Async WebSocket client for every DataMaxi+ WS data type.

Streams real-time data over the DataMaxi+ WebSocket API. Requires the ``ws``
extra::

    pip install "datamaxi[ws]"

Usage::

    from datamaxi.aio.ws import AsyncDatamaxiWS

    async with AsyncDatamaxiWS(api_key="...") as ws:
        async for msg in ws.ticker.subscribe("BTC-USDT@binance", market="spot"):
            print(msg["s"], msg["p"])

        async for oi in ws.open_interest.subscribe("BTC-USDT@binance"):
            ...

Channels (accessors driven by the generated ``WS_CHANNELS`` registry):
``ticker`` (market-keyed), ``forex``, ``premium``, ``funding_rate``,
``open_interest``, ``liquidation`` (subscribe), ``liquidation_feed``
(firehose, no params), ``announcement`` / ``announcement_internal`` (Pro+).

Consumes the **generated** WS surface — ``WS_CHANNELS`` / ``WS_BASE_PATH`` /
``WS_AUTH_HEADER`` from ``datamaxi._ws_endpoints`` and the per-channel message
models from ``datamaxi._ws_models`` (both emitted by datamaxi-codegen from the
backend). Orderbook is intentionally excluded (unsupported product).

Routing model: one connection per channel path, multiplexing all subscribed
``params``. ``subscribe()`` returns an async iterator over **every** message on
that channel — the WS protocol tags messages by payload fields (``s``/``e``),
not by a channel id, so callers filter by ``msg["s"]`` when subscribing to
multiple symbols on one connection.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any, AsyncIterator, Dict, List, Optional

from datamaxi.__version__ import __version__
from datamaxi._ws_endpoints import WS_CHANNELS, WS_BASE_PATH, WS_AUTH_HEADER

_DEFAULT_WS_URL = "wss://api.datamaxiplus.com"
# Send an app-level PING within the ~90s openresty proxy idle timeout.
_KEEPALIVE_INTERVAL = 30.0
_RECONNECT_BACKOFF = 1.0
_CLOSED = object()  # sentinel pushed to subscriber queues on shutdown


def _import_websockets():
    try:
        import websockets
    except ImportError as exc:  # pragma: no cover - exercised via extra
        raise ImportError(
            "The WebSocket client requires websockets. Install it with: "
            "pip install 'datamaxi[ws]'"
        ) from exc
    return websockets


def _derive_ws_url(base_url: Optional[str]) -> str:
    if not base_url:
        return _DEFAULT_WS_URL
    if base_url.startswith("https://"):
        return "wss://" + base_url.removeprefix("https://")
    if base_url.startswith("http://"):
        return "ws://" + base_url.removeprefix("http://")
    return base_url


class AsyncWSConnection:
    """One WebSocket connection to a single channel path.

    Owns the SUBSCRIBE / UNSUBSCRIBE / PING protocol, a reader that fans each
    incoming data message out to every subscriber stream, an app-level PING
    keepalive, and reconnect-with-resubscribe on a dropped connection.
    """

    def __init__(
        self,
        url: str,
        api_key: Optional[str],
        keepalive: float = _KEEPALIVE_INTERVAL,
        reconnect: bool = True,
        connect_kwargs: Optional[dict] = None,
    ):
        self._url = url
        self._api_key = api_key
        self._keepalive = keepalive
        self._reconnect = reconnect
        self._connect_kwargs = connect_kwargs or {}
        self._ws = None
        self._websockets = None
        self._id = 0
        self._active: set = set()  # params to replay on reconnect
        self._subscribers: List[asyncio.Queue] = []
        self._reader_task: Optional[asyncio.Task] = None
        self._keepalive_task: Optional[asyncio.Task] = None
        self._closed = False

    async def start(self) -> None:
        await self._open()
        self._reader_task = asyncio.create_task(self._reader())
        if self._keepalive:
            self._keepalive_task = asyncio.create_task(self._keepalive_loop())

    async def _open(self) -> None:
        self._websockets = _import_websockets()
        headers = {
            WS_AUTH_HEADER: str(self._api_key),
            "User-Agent": "datamaxi/" + __version__,
        }
        # No Origin header: coder/websocket enforces same-origin otherwise.
        self._ws = await self._websockets.connect(
            self._url, additional_headers=headers, **self._connect_kwargs
        )
        if self._active:  # resubscribe after a reconnect
            await self._send(
                {
                    "method": "SUBSCRIBE",
                    "params": sorted(self._active),
                    "id": self._next_id(),
                }
            )

    def _next_id(self) -> int:
        self._id += 1
        return self._id

    async def _send(self, obj: dict) -> None:
        await self._ws.send(json.dumps(obj))

    async def subscribe(self, params: List[str]) -> None:
        self._active.update(params)
        await self._send(
            {"method": "SUBSCRIBE", "params": list(params), "id": self._next_id()}
        )

    async def unsubscribe(self, params: List[str]) -> None:
        for p in params:
            self._active.discard(p)
        await self._send(
            {"method": "UNSUBSCRIBE", "params": list(params), "id": self._next_id()}
        )

    def stream(self) -> AsyncIterator[Dict[str, Any]]:
        """Register a subscriber queue *now* and return an iterator over it."""
        q: asyncio.Queue = asyncio.Queue()
        self._subscribers.append(q)
        return self._drain(q)

    async def _drain(self, q: asyncio.Queue) -> AsyncIterator[Dict[str, Any]]:
        try:
            while True:
                item = await q.get()
                if item is _CLOSED:
                    return
                yield item
        finally:
            if q in self._subscribers:
                self._subscribers.remove(q)

    async def _reader(self) -> None:
        while not self._closed:
            try:
                raw = await self._ws.recv()
            except self._websockets.ConnectionClosed:
                if self._closed or not self._reconnect:
                    break
                await asyncio.sleep(_RECONNECT_BACKOFF)
                try:
                    await self._open()
                except Exception:
                    continue
                else:
                    continue
            msg = json.loads(raw)
            # Subscription acks are {"result": [...], "id": N}; when the accepted
            # param list is empty the server omits `result`, leaving just
            # {"id": N}. Data payloads always carry other fields (s/e/d/...) —
            # note they may also include an "id" (token id), so detect an ack as
            # any dict whose keys are a subset of {"result", "id"}.
            if isinstance(msg, dict) and set(msg) <= {"result", "id"}:
                continue
            for q in list(self._subscribers):
                q.put_nowait(msg)
        for q in list(self._subscribers):
            q.put_nowait(_CLOSED)

    async def _keepalive_loop(self) -> None:
        while not self._closed:
            await asyncio.sleep(self._keepalive)
            try:
                await self._send({"method": "PING"})
            except Exception:
                pass

    async def close(self) -> None:
        self._closed = True
        for task in (self._reader_task, self._keepalive_task):
            if task is not None:
                task.cancel()
        if self._ws is not None:
            await self._ws.close()
        for q in list(self._subscribers):
            q.put_nowait(_CLOSED)


def _require_channel(path: str) -> str:
    if path not in WS_CHANNELS:
        raise ValueError(
            f"unknown WS channel {path!r}; generated: {sorted(WS_CHANNELS)}"
        )
    return path


class Subscription:
    """A single-path subscribable channel (``ws.forex``, ``ws.premium``, ...).

    ``param_format`` echoes the generated registry's subscribe param format for
    reference; callers pass the raw param strings (e.g. ``"BTC-USDT@binance"``).
    """

    def __init__(self, client: "AsyncDatamaxiWS", path: str):
        self._client = client
        self._path = _require_channel(path)

    @property
    def param_format(self) -> Optional[str]:
        return WS_CHANNELS[self._path].get("param")

    async def subscribe(self, *params: str) -> AsyncIterator[Dict[str, Any]]:
        """SUBSCRIBE to ``params``; return an async iterator over the channel."""
        conn = await self._client._conn(self._path)
        stream = conn.stream()  # register the queue before SUBSCRIBE (no missed msgs)
        await conn.subscribe(list(params))
        return stream

    async def unsubscribe(self, *params: str) -> None:
        conn = await self._client._conn(self._path)
        await conn.unsubscribe(list(params))


class MarketSubscription:
    """A market-keyed subscribable channel (``ws.ticker``) → ``<base>/<market>``."""

    def __init__(self, client: "AsyncDatamaxiWS", base: str):
        self._client = client
        self._base = base

    def _path(self, market: str) -> str:
        path = f"{self._base}/{market}"
        if path not in WS_CHANNELS:
            valid = [p for p in WS_CHANNELS if p.startswith(self._base + "/")]
            raise ValueError(f"unknown market {market!r}; valid paths: {valid}")
        return path

    async def subscribe(
        self, *params: str, market: str = "spot"
    ) -> AsyncIterator[Dict[str, Any]]:
        conn = await self._client._conn(self._path(market))
        stream = conn.stream()
        await conn.subscribe(list(params))
        return stream

    async def unsubscribe(self, *params: str, market: str = "spot") -> None:
        conn = await self._client._conn(self._path(market))
        await conn.unsubscribe(list(params))


class Feed:
    """A firehose channel (``ws.liquidation_feed``) — auto-subscribed, no params."""

    def __init__(self, client: "AsyncDatamaxiWS", path: str):
        self._client = client
        self._path = _require_channel(path)

    async def stream(self) -> AsyncIterator[Dict[str, Any]]:
        conn = await self._client._conn(self._path)
        return conn.stream()


class AsyncDatamaxiWS:
    """Async WebSocket entrypoint — every DataMaxi+ WS data type.

    Accessors are driven by the generated ``WS_CHANNELS`` registry:
    ``ticker`` (market-keyed), ``forex``, ``premium``, ``funding_rate``,
    ``open_interest``, ``liquidation`` (subscribe), ``liquidation_feed``
    (firehose), ``announcement`` / ``announcement_internal`` (Pro+).

    Use as an async context manager so open connections are closed, or call
    :meth:`aclose` explicitly.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        ws_url: Optional[str] = None,
        base_url: Optional[str] = None,
        keepalive: float = _KEEPALIVE_INTERVAL,
        reconnect: bool = True,
        connect_kwargs: Optional[dict] = None,
    ):
        self.api_key = api_key or os.environ.get("DATAMAXI_API_KEY")
        self.ws_url = ws_url or _derive_ws_url(base_url)
        self._keepalive = keepalive
        self._reconnect = reconnect
        self._connect_kwargs = connect_kwargs
        self._conns: Dict[str, AsyncWSConnection] = {}

        self.ticker = MarketSubscription(self, "/ticker")
        self.forex = Subscription(self, "/forex")
        self.premium = Subscription(self, "/premium")
        self.funding_rate = Subscription(self, "/funding-rate")
        self.open_interest = Subscription(self, "/open-interest")
        self.liquidation = Subscription(self, "/liquidation")
        self.liquidation_feed = Feed(self, "/liquidation/feed")
        self.announcement = Subscription(self, "/announcement/listing")
        self.announcement_internal = Subscription(
            self, "/announcement/listing/internal"
        )

    async def _conn(self, path: str) -> AsyncWSConnection:
        conn = self._conns.get(path)
        if conn is None:
            url = self.ws_url + WS_BASE_PATH + path
            conn = AsyncWSConnection(
                url,
                self.api_key,
                keepalive=self._keepalive,
                reconnect=self._reconnect,
                connect_kwargs=self._connect_kwargs,
            )
            await conn.start()
            self._conns[path] = conn
        return conn

    async def aclose(self) -> None:
        for conn in list(self._conns.values()):
            await conn.close()
        self._conns.clear()

    async def __aenter__(self) -> "AsyncDatamaxiWS":
        return self

    async def __aexit__(self, *exc) -> None:
        await self.aclose()

    def __repr__(self) -> str:
        return "AsyncDatamaxiWS(ws_url={!r}, has_key={})".format(
            self.ws_url, bool(self.api_key)
        )
