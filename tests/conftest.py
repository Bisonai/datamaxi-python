"""Shared test fixtures, constants, and markers.

Centralizes the API key / base URL resolution, the live client fixtures
(``datamaxi`` / ``telegram`` / ``naver``), and the ``_FLAKY_PROD_DATA_XFAIL``
marker that ``test_call.py`` and ``test_integration.py`` previously
copy-pasted verbatim.
"""

import os
import pytest

from datamaxi import Datamaxi, Telegram, Naver

# Live-test credentials / target. Resolved once so the keyed lanes
# (test_call.py, test_integration.py) share a single source of truth; both
# honor DATAMAXI_API_KEY (preferred) and the legacy API_KEY.
API_KEY = os.getenv("DATAMAXI_API_KEY") or os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"

# Shared xfail marker for tests whose outcome depends on prod-data
# availability — funding-rate / naver-trend state are NATS-warmed in-memory
# caches on the API pods, so any cold-start of the API fleet leaves them
# temporarily empty and the smoke-style tests raise ServerError(500, "no data
# found"). Marked strict=False so they pass cleanly once the cache is hot.
_FLAKY_PROD_DATA_XFAIL = pytest.mark.xfail(
    reason=(
        "Depends on prod NATS-warmed state; intermittent 500 'no data found' "
        "on cold pods. Pre-existing flakiness — unrelated to SDK regen."
    ),
    strict=False,
)


@pytest.fixture(scope="module")
def datamaxi():
    """Create Datamaxi client for live tests."""
    return Datamaxi(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def telegram():
    """Create Telegram client for live tests."""
    return Telegram(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def naver():
    """Create Naver client for live tests."""
    return Naver(api_key=API_KEY, base_url=BASE_URL)
