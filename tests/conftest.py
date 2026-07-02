"""Shared test fixtures and constants.

Centralizes the API key / base URL resolution and the live client fixtures
(``datamaxi`` / ``telegram`` / ``naver``).
"""

import os
import pytest

from datamaxi import Datamaxi, Telegram, Naver

# Live-test credentials / target. Resolved once so the keyed lanes
# (test_call.py, test_integration.py) share a single source of truth; both
# honor DATAMAXI_API_KEY (preferred) and the legacy API_KEY.
API_KEY = os.getenv("DATAMAXI_API_KEY") or os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"
# Live-lane timeout: larger than the SDK's 10s default so slow prod endpoints
# (e.g. unfiltered premium) don't ReadTimeout on the smoke/integration tests.
TIMEOUT = int(os.getenv("DATAMAXI_TIMEOUT") or "30")


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
