"""Tests for the shared retry policy (``datamaxi._retry``, see #154).

Covers the pure policy functions directly, plus the async transport's use of
them: GET-only, exponential backoff, and honoring ``Retry-After`` — aligning
the ``httpx``-based async client with the ``urllib3``-backed sync retry
policy exercised in ``tests/test_retry.py``.
"""

import asyncio

import pytest

from datamaxi._retry import (
    is_retryable,
    parse_retry_after,
    get_backoff_time,
    get_retry_delay,
)

httpx = pytest.importorskip("httpx")

from datamaxi.aio._core import AsyncAPI  # noqa: E402

BASE_URL = "https://api.datamaxiplus.com"


# --- pure policy functions ---------------------------------------------------
def test_is_retryable_get_only():
    assert is_retryable("GET", 503, 1, 3, (502, 503, 504))
    assert is_retryable("get", 503, 1, 3, (502, 503, 504))  # case-insensitive
    assert not is_retryable("POST", 503, 1, 3, (502, 503, 504))


def test_is_retryable_only_for_listed_statuses():
    assert not is_retryable("GET", 200, 1, 3, (502, 503, 504))


def test_is_retryable_respects_max_retries():
    assert is_retryable("GET", 503, 3, 3, (503,))
    assert not is_retryable("GET", 503, 4, 3, (503,))


def test_get_backoff_time_is_exponential_with_zero_first_retry():
    # Matches urllib3.Retry.get_backoff_time(): no delay before the first
    # retry, then backoff_factor * 2 ** (n - 1).
    assert get_backoff_time(1, 0.5) == 0.0
    assert get_backoff_time(2, 0.5) == 1.0
    assert get_backoff_time(3, 0.5) == 2.0
    assert get_backoff_time(4, 0.5) == 4.0


def test_get_backoff_time_caps_at_backoff_max():
    assert get_backoff_time(20, 10.0) == 120.0


def test_parse_retry_after_seconds_form():
    assert parse_retry_after("120") == 120.0


def test_parse_retry_after_missing_returns_none():
    assert parse_retry_after(None) is None


def test_parse_retry_after_never_negative():
    # An HTTP-date in the past yields a would-be-negative delta.
    assert parse_retry_after("Mon, 01 Jan 2001 00:00:00 GMT") == 0.0


def test_get_retry_delay_prefers_retry_after_header():
    assert get_retry_delay(4, 0.5, {"Retry-After": "7"}) == 7.0


def test_get_retry_delay_falls_back_to_backoff():
    assert get_retry_delay(3, 0.5, {}) == 2.0


# --- async transport wiring ---------------------------------------------------
def _run(coro):
    return asyncio.run(coro)


def test_async_get_retries_transient_5xx_with_exponential_backoff(monkeypatch):
    sleeps = []

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 4:
            return httpx.Response(503, json={"error": "busy"})
        return httpx.Response(200, json={"ok": True})

    async def run():
        api = AsyncAPI(
            api_key="k",
            base_url=BASE_URL,
            max_retries=3,
            retry_backoff=0.5,
            transport=httpx.MockTransport(handler),
        )
        try:
            return await api.send_request("GET", "/x")
        finally:
            await api.aclose()

    data = _run(run())
    assert data == {"ok": True}
    assert calls["n"] == 4
    # No delay before the 1st retry, then exponential growth (factor * 2**(n-1)).
    assert sleeps == [0.0, 1.0, 2.0]


def test_async_post_is_not_retried(monkeypatch):
    async def fake_sleep(seconds):
        raise AssertionError("POST must not be retried")

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        return httpx.Response(503, json={"error": "busy"})

    async def run():
        api = AsyncAPI(
            api_key="k",
            base_url=BASE_URL,
            max_retries=3,
            transport=httpx.MockTransport(handler),
        )
        try:
            await api.send_request("POST", "/x")
        finally:
            await api.aclose()

    from datamaxi.error import ServerError

    with pytest.raises(ServerError):
        _run(run())
    assert calls["n"] == 1


def test_async_honors_retry_after_header(monkeypatch):
    sleeps = []

    async def fake_sleep(seconds):
        sleeps.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)

    calls = {"n": 0}

    def handler(request):
        calls["n"] += 1
        if calls["n"] < 2:
            return httpx.Response(
                503, json={"error": "busy"}, headers={"Retry-After": "3"}
            )
        return httpx.Response(200, json={"ok": True})

    async def run():
        api = AsyncAPI(
            api_key="k",
            base_url=BASE_URL,
            max_retries=3,
            retry_backoff=0.5,
            transport=httpx.MockTransport(handler),
        )
        try:
            return await api.send_request("GET", "/x")
        finally:
            await api.aclose()

    data = _run(run())
    assert data == {"ok": True}
    # Retry-After (3s) takes priority over the computed backoff (0s).
    assert sleeps == [3.0]
