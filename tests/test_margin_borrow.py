"""Local (mocked) tests for the MarginBorrow client."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.resources.margin_borrow import MarginBorrow
from datamaxi.error import ParameterRequiredError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"


def _mb():
    return MarginBorrow(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/margin-borrow", {"data": {}})
def test_margin_borrow_returns_dict():
    assert _mb()(asset="BTC") == {"data": {}}


@responses.activate
def test_margin_borrow_forwards_asset():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/margin-borrow.*"),
        json={"data": {}},
        status=200,
    )
    _mb()(asset="BTC")
    qs = _qs(responses.calls[0])
    assert qs["asset"] == ["BTC"]


def test_margin_borrow_missing_asset_raises():
    with pytest.raises(ParameterRequiredError):
        _mb()(asset="")
