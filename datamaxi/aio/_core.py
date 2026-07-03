"""Async transport core — ``httpx``-based, shared by all async resources.

Reuses the sync client's endpoint resolution and error handling
(``datamaxi._dispatch``) plus ``ResponseMeta``, so the sync and async clients
can't drift on request building or error semantics.
"""

import asyncio
import os

from datamaxi.__version__ import __version__
from datamaxi.api import ResponseMeta
from datamaxi._dispatch import resolve_endpoint, raise_for_error, extract_limit_usage


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
