"""Shared test fixtures and constants.

Centralizes the API key / base URL resolution and the live client fixtures
(``datamaxi`` / ``telegram`` / ``naver``).
"""

import os
import time

import pytest

from datamaxi import Datamaxi, Telegram, Naver
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


def live_call(fn, retries=3, backoff=1.0):
    """Invoke a live-endpoint call, tolerating transient gateway errors.

    Retries ``fn`` on a transient 5xx (``_TRANSIENT_STATUS``) with linear
    backoff. If every attempt still hits a transient status the call is
    ``pytest.skip``-ped rather than failed — the non-blocking live lane must
    not go red on prod infra flakiness. Any other error (real 5xx, 4xx,
    assertion) propagates unchanged.
    """
    for attempt in range(retries):
        try:
            return fn()
        except ServerError as e:
            if e.status_code not in _TRANSIENT_STATUS:
                raise
            if attempt == retries - 1:
                pytest.skip(
                    "transient %s from live endpoint after %d attempts"
                    % (e.status_code, retries)
                )
            time.sleep(backoff * (attempt + 1))


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
