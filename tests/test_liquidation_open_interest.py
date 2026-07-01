"""Local (mocked) happy-path + error tests for Liquidation / OpenInterest.

Query-param translation (topN -> top_n) is covered in test_query_params.py;
this file adds return-shape and error-handling coverage.
"""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.liquidation import Liquidation
from datamaxi.datamaxi.open_interest import OpenInterest
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"


def _liq():
    return Liquidation(api_key="key", base_url=BASE_URL)


def _oi():
    return OpenInterest(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/liquidation", {"data": [{"id": 1}]})
def test_liquidation_call_returns_dict():
    res = _liq()(exchange="binance", symbol="BTC-USDT")
    assert res == {"data": [{"id": 1}]}


@responses.activate
def test_liquidation_call_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/liquidation.*"),
        json={"data": []},
        status=200,
    )
    _liq()(exchange="binance", symbol="BTC-USDT", limit=5)
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["symbol"] == ["BTC-USDT"]
    assert qs["limit"] == ["5"]


@mock_http_response(responses.GET, "/api/v1/liquidation/feed", {"data": []})
def test_liquidation_feed_returns_dict():
    assert _liq().feed(limit=10) == {"data": []}


@responses.activate
def test_liquidation_feed_forwards_new_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/liquidation/feed.*"),
        json={"data": []},
        status=200,
    )
    _liq().feed(limit=10, exchange="binance", base="BTC", min_volume_usd=1000.0)
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["base"] == ["BTC"]
    assert qs["min_volume_usd"] == ["1000.0"]


def test_liquidation_invalid_limit_raises_value_error():
    with pytest.raises(ValueError):
        _liq()(exchange="binance", symbol="BTC-USDT", limit=0)


def test_liquidation_heatmap_invalid_top_n_raises_value_error():
    with pytest.raises(ValueError):
        _liq().heatmap(topN=99)


@mock_http_response(
    responses.GET, "/api/v1/liquidation", {"error": "bad request"}, http_status=400
)
def test_liquidation_client_error():
    with pytest.raises(ClientError):
        _liq()(exchange="binance", symbol="BTC-USDT")


@mock_http_response(
    responses.GET, "/api/v1/liquidation", {"error": "boom"}, http_status=500
)
def test_liquidation_server_error():
    with pytest.raises(ServerError):
        _liq()(exchange="binance", symbol="BTC-USDT")


@mock_http_response(responses.GET, "/api/v1/open-interest", {"oi": "100"})
def test_open_interest_call_returns_dict():
    assert _oi()(exchange="binance", symbol="BTC-USDT") == {"oi": "100"}


@responses.activate
def test_open_interest_history_aggregated_sends_from_to():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/open-interest/history-aggregated.*"),
        json={"data": []},
        status=200,
    )
    _oi().history_aggregated(token_id="bitcoin", from_=111, to=222)
    qs = _qs(responses.calls[0])
    assert qs["token_id"] == ["bitcoin"]
    assert qs["from"] == ["111"]
    assert qs["to"] == ["222"]


@mock_http_response(responses.GET, "/api/v1/open-interest/list", {"data": []})
def test_open_interest_list_returns_dict():
    assert _oi().list(exchange="binance") == {"data": []}


def test_open_interest_overview_invalid_sort_raises_value_error():
    with pytest.raises(ValueError):
        _oi().overview(sort="bogus")


@mock_http_response(
    responses.GET, "/api/v1/open-interest", {"error": "bad request"}, http_status=400
)
def test_open_interest_client_error():
    with pytest.raises(ClientError):
        _oi()(exchange="binance", symbol="BTC-USDT")


@mock_http_response(
    responses.GET, "/api/v1/open-interest", {"error": "boom"}, http_status=500
)
def test_open_interest_server_error():
    with pytest.raises(ServerError):
        _oi()(exchange="binance", symbol="BTC-USDT")
