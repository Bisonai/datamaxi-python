"""Anti-drift check: the async premium resource reuses the sync module's
param-builder / response-shaper (see #154) rather than a hand-copied one.
"""

import pytest

httpx = pytest.importorskip("httpx")

from datamaxi.aio import premium as aio_premium  # noqa: E402
from datamaxi.resources import premium as sync_premium  # noqa: E402


def test_async_premium_reuses_sync_param_builder():
    assert aio_premium.build_premium_params is sync_premium.build_premium_params


def test_async_premium_reuses_sync_response_shaper():
    assert aio_premium.shape_premium_response is sync_premium.shape_premium_response
