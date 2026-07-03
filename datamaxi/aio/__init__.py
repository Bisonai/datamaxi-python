"""Async client (pilot) — ``httpx``-based, mirrors a slice of the sync surface.

Requires the ``async`` extra::

    pip install "datamaxi[async]"

Usage::

    from datamaxi.aio import AsyncDatamaxi

    async with AsyncDatamaxi(api_key="...") as client:
        df = await client.cex.candle(exchange="binance", market="spot",
                                     symbol="BTC-USDT")
        ticker = await client.cex.ticker.get(exchange="binance", market="spot",
                                             symbol="BTC-USDT")

This is a deliberately small pilot (candle + ticker). It reuses the sync
client's endpoint resolution and error handling (``datamaxi._dispatch``) and
the shared DataFrame / ResponseMeta helpers, so the two clients can't drift on
request building or error semantics.
"""

from __future__ import annotations

import asyncio
import os
from typing import Any, Union, TYPE_CHECKING

from datamaxi.__version__ import __version__
from datamaxi.api import ResponseMeta
from datamaxi._dispatch import resolve_endpoint, raise_for_error, extract_limit_usage
from datamaxi.lib.constants import (
    BASE_URL,
    SPOT,
    FUTURES,
    USD,
    INTERVAL_1D,
    Market,
    Interval,
)
from datamaxi.lib.utils import check_required_parameters
from datamaxi.resources.responses import CandleResponse, TickerResponse

if TYPE_CHECKING:
    import pandas as pd


def _import_httpx():
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover - exercised via extra
        raise ImportError(
            "The async client requires httpx. Install it with: "
            "pip install 'datamaxi[async]'"
        ) from exc
    return httpx


class AsyncAPI:
    """Async transport built on ``httpx.AsyncClient``.

    Mirrors the sync ``API``: shared endpoint resolution, bounded retry of
    transient gateway 5xx, the same ``ClientError`` / ``ServerError`` contract,
    and ``last_response`` metadata.
    """

    def __init__(
        self,
        api_key=None,
        base_url=None,
        timeout=10,
        max_retries=3,
        retry_backoff=0.5,
        retry_statuses=(502, 503, 504),
        transport=None,
    ):
        httpx = _import_httpx()
        self.api_key = api_key or os.environ.get("DATAMAXI_API_KEY")
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.retry_statuses = tuple(retry_statuses)
        self.last_response = None
        self._client = httpx.AsyncClient(
            base_url=base_url or "",
            timeout=timeout,
            transport=transport,
            headers={
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "datamaxi/" + __version__,
                "X-DTMX-APIKEY": str(self.api_key),
            },
        )

    async def request_endpoint(self, op_id, **params):
        method, url_path, query_params = resolve_endpoint(op_id, **params)
        return await self.send_request(method, url_path, payload=query_params)

    async def send_request(self, method, url_path, payload=None):
        # str()-encode scalars so bools match the sync client's urlencode
        # output (e.g. include_source -> "True", not httpx's "true").
        params = {k: str(v) for k, v in (payload or {}).items() if v is not None}
        for attempt in range(self.max_retries + 1):
            response = await self._client.request(method, url_path, params=params)
            if (
                response.status_code in self.retry_statuses
                and attempt < self.max_retries
            ):
                await asyncio.sleep(self.retry_backoff * (attempt + 1))
                continue
            break

        raise_for_error(response.status_code, response.text, response.headers)

        try:
            data = response.json()
        except ValueError:
            data = response.text

        self.last_response = ResponseMeta(
            status_code=response.status_code,
            headers=response.headers,
            limit_usage=extract_limit_usage(response.headers),
            data=data,
        )
        return data

    async def aclose(self):
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()


class AsyncResource:
    """Base for async resources — composes a shared ``AsyncAPI``."""

    def __init__(self, api: "AsyncAPI"):
        self._api = api

    async def request_endpoint(self, op_id, **params):
        return await self._api.request_endpoint(op_id, **params)

    @property
    def last_response(self):
        return self._api.last_response


class AsyncCexCandle(AsyncResource):
    async def __call__(
        self,
        exchange: str,
        market: Market,
        symbol: str,
        currency: str = USD,
        interval: Interval = INTERVAL_1D,
        from_unix: str = None,
        to_unix: str = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, CandleResponse]:
        """Fetch candle data (async). See ``datamaxi.Datamaxi.cex.candle``."""
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [interval, "interval"],
                [market, "market"],
                [currency, "currency"],
            ]
        )
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        res = await self.request_endpoint(
            "cex_candle",
            exchange=exchange,
            market=market,
            symbol=symbol,
            interval=interval,
            currency=currency,
            **{"from": from_unix, "to": to_unix},
        )
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        if pandas:
            from datamaxi.resources.utils import convert_data_to_data_frame

            return convert_data_to_data_frame(res["data"])
        return res


class AsyncCexTicker(AsyncResource):
    async def get(
        self,
        exchange: str,
        symbol: str,
        market: Market,
        currency: str = None,
        conversion_base: str = None,
        include_source: bool = False,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, TickerResponse]:
        """Fetch ticker data (async). See ``datamaxi.Datamaxi.cex.ticker``."""
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [market, "market"],
            ]
        )
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        res = await self.request_endpoint(
            "ticker",
            exchange=exchange,
            symbol=symbol,
            market=market,
            currency=currency,
            conversion_base=conversion_base,
            include_source=include_source,
        )

        if pandas:
            import pandas as pd

            df = pd.DataFrame([res["data"]])
            df = df.set_index("d")
            return df
        return res


class AsyncCex(AsyncResource):
    def __init__(self, api: "AsyncAPI"):
        super().__init__(api)
        self.candle = AsyncCexCandle(api)
        self.ticker = AsyncCexTicker(api)


class AsyncDatamaxi:
    """Async entrypoint (pilot). Exposes ``cex.candle`` and ``cex.ticker``.

    Use as an async context manager so the underlying ``httpx`` client is
    closed, or call :meth:`aclose` explicitly.
    """

    def __init__(self, api_key=None, **kwargs: Any):
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        self._api = AsyncAPI(api_key, **kwargs)
        self.cex = AsyncCex(self._api)

    async def aclose(self):
        await self._api.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.aclose()

    def __repr__(self):
        return "AsyncDatamaxi(base_url={!r}, has_key={})".format(
            self._api.base_url, bool(self._api.api_key)
        )


__all__ = [
    "AsyncDatamaxi",
    "AsyncAPI",
    "AsyncResource",
    "AsyncCex",
    "AsyncCexCandle",
    "AsyncCexTicker",
]
