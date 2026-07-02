"""Shared test fixtures and constants.

Centralizes the API key / base URL resolution and the live client fixtures
(``datamaxi`` / ``telegram`` / ``naver``).
"""

import os
import time

import pytest

from datamaxi import Datamaxi, Telegram, Naver
from datamaxi.api import API
from datamaxi.error import ServerError

# Transient gateway statuses: the prod edge returns these when an upstream is
# briefly slow/unavailable (e.g. the premium endpoint 504-ing under load). They
# are infra flakiness, not SDK bugs, so the live lane retries then skips.
_TRANSIENT_STATUS = (502, 503, 504)

# Live-test credentials / target. Resolved once so the keyed lanes
# (test_call.py, test_integration.py) share a single source of truth; both
# honor DATAMAXI_API_KEY (preferred) and the legacy API_KEY.
API_KEY = os.getenv("DATAMAXI_API_KEY") or os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"
# Live-lane timeout: larger than the SDK's 10s default so slow prod endpoints
# (e.g. unfiltered premium) don't ReadTimeout on the smoke/integration tests.
TIMEOUT = int(os.getenv("DATAMAXI_TIMEOUT") or "30")


@pytest.fixture(autouse=True)
def _tolerate_transient_gateway(monkeypatch):
    """Retry transient gateway 5xx at the HTTP boundary for every live call.

    The keyed live lane hits prod, whose edge intermittently returns a
    ``_TRANSIENT_STATUS`` (502/503/504) under load — infra flakiness, not an SDK
    bug. Wrapping ``API.send_request`` (the single method every endpoint object
    inherits) makes EVERY live call across ``test_call.py`` and
    ``test_integration.py`` retry with linear backoff, then ``pytest.skip`` if
    still transient — so the non-blocking lane never goes red on a transient
    prod 5xx, without per-test wrapping. Real 5xx/4xx and assertions propagate
    on the first attempt.

    No-op without a key: the keyless/mocked lanes are skipped (``API_KEY``
    unset) or mock the transport, so they never raise a transient ``ServerError``
    and stay untouched.
    """
    if not API_KEY:
        return

    retries, backoff = 3, 1.0
    original = API.send_request

    def retrying(self, *args, **kwargs):
        for attempt in range(retries):
            try:
                return original(self, *args, **kwargs)
            except ServerError as e:
                if e.status_code not in _TRANSIENT_STATUS:
                    raise
                if attempt == retries - 1:
                    pytest.skip(
                        "transient %s from live endpoint after %d attempts"
                        % (e.status_code, retries)
                    )
                time.sleep(backoff * (attempt + 1))

    monkeypatch.setattr(API, "send_request", retrying)


@pytest.fixture(scope="module")
def datamaxi():
    """Create Datamaxi client for live tests."""
    return Datamaxi(api_key=API_KEY, base_url=BASE_URL, timeout=TIMEOUT)


@pytest.fixture(scope="module")
def telegram():
    """Create Telegram client for live tests."""
    return Telegram(api_key=API_KEY, base_url=BASE_URL, timeout=TIMEOUT)


@pytest.fixture(scope="module")
def naver():
    """Create Naver client for live tests."""
    return Naver(api_key=API_KEY, base_url=BASE_URL, timeout=TIMEOUT)
