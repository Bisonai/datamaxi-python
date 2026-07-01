"""Local (mocked) tests for the CexSymbol client. No API key / network."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.cex_symbol import CexSymbol
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"


def _client():
    return CexSymbol(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(
    responses.GET, "/api/v1/cex/symbol/metadata", {"BTC": {"status": "trading"}}
)
def test_metadata_returns_dict():
    res = _client().metadata(exchange="binance", base="BTC")
    assert res == {"BTC": {"status": "trading"}}


@responses.activate
def test_metadata_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/symbol/metadata.*"),
        json={},
        status=200,
    )
    _client().metadata(exchange="binance", base="BTC")
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["base"] == ["BTC"]


@mock_http_response(responses.GET, "/api/v1/cex/symbol/tags", {"BTC": ["seed"]})
def test_tags_returns_dict():
    assert _client().tags(base="BTC") == {"BTC": ["seed"]}


@mock_http_response(responses.GET, "/api/v1/cex/symbol/cautions", {"BTC": []})
def test_cautions_returns_dict():
    assert _client().cautions(exchange="binance") == {"BTC": []}


@mock_http_response(responses.GET, "/api/v1/cex/symbol/delistings", {"BTC": []})
def test_delistings_returns_dict():
    assert _client().delistings(exchange="binance") == {"BTC": []}


@responses.activate
def test_volume_sends_base_param():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/symbol/volume.*"),
        json={"BTC": {"binance": "100"}},
        status=200,
    )
    res = _client().volume(base="BTC")
    qs = _qs(responses.calls[0])
    assert qs["base"] == ["BTC"]
    assert res == {"BTC": {"binance": "100"}}


@mock_http_response(responses.GET, "/api/v1/cex/symbol/oi", {"BTC": {"binance": "1"}})
def test_oi_returns_dict():
    assert _client().oi(base="BTC") == {"BTC": {"binance": "1"}}


@responses.activate
def test_oi_stats_sends_currency_param():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/symbol/oi-stats.*"),
        json={"BTC": {}},
        status=200,
    )
    _client().oi_stats(base="BTC", currency="KRW")
    qs = _qs(responses.calls[0])
    assert qs["base"] == ["BTC"]
    assert qs["currency"] == ["KRW"]


def test_oi_stats_invalid_currency_raises_value_error():
    with pytest.raises(ValueError):
        _client().oi_stats(base="BTC", currency="EUR")


@responses.activate
def test_liquidation_sends_window_param():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/symbol/liquidation.*"),
        json={"BTC": {}},
        status=200,
    )
    _client().liquidation(base="BTC", window="7d")
    qs = _qs(responses.calls[0])
    assert qs["base"] == ["BTC"]
    assert qs["window"] == ["7d"]


@mock_http_response(
    responses.GET,
    "/api/v1/cex/symbol/metadata",
    {"error": "bad request"},
    http_status=400,
)
def test_metadata_client_error():
    with pytest.raises(ClientError):
        _client().metadata(base="BTC")


@mock_http_response(
    responses.GET, "/api/v1/cex/symbol/metadata", {"error": "boom"}, http_status=500
)
def test_metadata_server_error():
    with pytest.raises(ServerError):
        _client().metadata(base="BTC")
