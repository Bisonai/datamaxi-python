"""Local (mocked) tests for the CexTicker client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.resources.cex_ticker import CexTicker
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_TICKER = {"data": {"d": "1700000000", "p": "105.5"}}


def _client():
    return CexTicker(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/ticker", _TICKER)
def test_ticker_get_returns_dataframe():
    df = _client().get(exchange="binance", market="spot", symbol="BTC-USDT")
    assert isinstance(df, pd.DataFrame)
    assert "p" in df.columns
    assert len(df) == 1


@responses.activate
def test_ticker_get_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/ticker.*"),
        json=_TICKER,
        status=200,
    )
    _client().get(
        exchange="binance",
        market="spot",
        symbol="BTC-USDT",
        conversion_base="USDT",
    )
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["market"] == ["spot"]
    assert qs["symbol"] == ["BTC-USDT"]
    assert qs["conversion_base"] == ["USDT"]


def test_ticker_invalid_market_raises_value_error():
    with pytest.raises(ValueError):
        _client().get(exchange="binance", market="bogus", symbol="BTC-USDT")


@mock_http_response(responses.GET, "/api/v1/ticker/exchanges", ["binance", "okx"])
def test_ticker_exchanges_returns_list():
    assert _client().exchanges(market="spot") == ["binance", "okx"]


@mock_http_response(responses.GET, "/api/v1/ticker/symbols", ["BTC-USDT", "ETH-USDT"])
def test_ticker_symbols_returns_list():
    assert _client().symbols(exchange="binance", market="spot") == [
        "BTC-USDT",
        "ETH-USDT",
    ]


@mock_http_response(
    responses.GET, "/api/v1/ticker", {"error": "bad request"}, http_status=400
)
def test_ticker_client_error():
    with pytest.raises(ClientError):
        _client().get(exchange="binance", market="spot", symbol="BTC-USDT")


@mock_http_response(responses.GET, "/api/v1/ticker", {"error": "boom"}, http_status=500)
def test_ticker_server_error():
    with pytest.raises(ServerError):
        _client().get(exchange="binance", market="spot", symbol="BTC-USDT")
