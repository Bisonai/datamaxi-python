"""Local (mocked) tests for the CexFee client. No API key / network."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.cex_fee import CexFee
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_FEE = [{"exchange": "binance", "symbol": "BTC-USDT", "maker": "0.001"}]


def _client():
    return CexFee(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/cex/fees", _FEE)
def test_fee_call_returns_list():
    res = _client()(exchange="binance", symbol="BTC-USDT")
    assert res == _FEE


@responses.activate
def test_fee_call_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/fees.*"),
        json=_FEE,
        status=200,
    )
    _client()(exchange="binance", symbol="BTC-USDT")
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["symbol"] == ["BTC-USDT"]


@mock_http_response(responses.GET, "/api/v1/cex/fees/exchanges", ["binance", "okx"])
def test_fee_exchanges_returns_list():
    assert _client().exchanges() == ["binance", "okx"]


@mock_http_response(responses.GET, "/api/v1/cex/fees/symbols", ["BTC-USDT", "ETH-USDT"])
def test_fee_symbols_returns_list():
    assert _client().symbols(exchange="binance") == ["BTC-USDT", "ETH-USDT"]


@mock_http_response(
    responses.GET, "/api/v1/cex/fees", {"error": "bad request"}, http_status=400
)
def test_fee_client_error():
    with pytest.raises(ClientError):
        _client()(exchange="binance")


@mock_http_response(
    responses.GET, "/api/v1/cex/fees", {"error": "boom"}, http_status=500
)
def test_fee_server_error():
    with pytest.raises(ServerError):
        _client()(exchange="binance")
