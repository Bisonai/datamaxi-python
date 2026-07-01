"""Local (mocked) tests for the IndexPrice client."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.index_price import IndexPrice
from datamaxi.error import ParameterRequiredError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"


def _ip():
    return IndexPrice(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/index-price", {"data": []})
def test_index_price_returns_dict():
    assert _ip()(asset="BTC") == {"data": []}


@responses.activate
def test_index_price_forwards_params_with_from_to():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/index-price.*"),
        json={"data": []},
        status=200,
    )
    _ip()(asset="BTC", from_="2024-01-01", to="2024-02-01", interval="15m")
    qs = _qs(responses.calls[0])
    assert qs["asset"] == ["BTC"]
    assert qs["from"] == ["2024-01-01"]
    assert qs["to"] == ["2024-02-01"]
    assert qs["interval"] == ["15m"]


def test_index_price_missing_asset_raises():
    with pytest.raises(ParameterRequiredError):
        _ip()(asset="")
