"""Local (mocked) tests for the FundingRate client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.funding_rate import FundingRate
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_HISTORY = {"data": [{"d": "1700000000", "r": "0.0001"}]}
_LATEST = {"d": "1700000000", "r": "0.0001", "symbol": "BTC-USDT"}


def _client():
    return FundingRate(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/funding-rate/history", _HISTORY)
def test_history_returns_dataframe_and_next():
    df, next_request = _client().history(exchange="binance", symbol="BTC-USDT")
    assert isinstance(df, pd.DataFrame)
    assert callable(next_request)
    assert "r" in df.columns


@responses.activate
def test_history_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/funding-rate/history.*"),
        json=_HISTORY,
        status=200,
    )
    _client().history(exchange="binance", symbol="BTC-USDT", limit=50)
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["symbol"] == ["BTC-USDT"]
    assert qs["limit"] == ["50"]
    assert qs["sort"] == ["desc"]
    assert "from" not in qs and "to" not in qs


@mock_http_response(responses.GET, "/api/v1/funding-rate/latest", _LATEST)
def test_latest_returns_dataframe():
    df = _client().latest(exchange="binance", symbol="BTC-USDT")
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["symbol"] == "BTC-USDT"


@mock_http_response(
    responses.GET, "/api/v1/funding-rate/exchanges", ["binance", "bybit"]
)
def test_exchanges_returns_list():
    assert _client().exchanges() == ["binance", "bybit"]


@mock_http_response(
    responses.GET, "/api/v1/funding-rate/symbols", ["BTC-USDT", "ETH-USDT"]
)
def test_symbols_returns_list():
    assert _client().symbols(exchange="binance") == ["BTC-USDT", "ETH-USDT"]


@mock_http_response(
    responses.GET,
    "/api/v1/funding-rate/history",
    {"error": "bad request"},
    http_status=400,
)
def test_history_client_error():
    with pytest.raises(ClientError):
        _client().history(exchange="binance", symbol="BTC-USDT")


@mock_http_response(
    responses.GET, "/api/v1/funding-rate/latest", {"error": "boom"}, http_status=500
)
def test_latest_server_error():
    with pytest.raises(ServerError):
        _client().latest(exchange="binance", symbol="BTC-USDT")
