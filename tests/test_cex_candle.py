"""Local (mocked) tests for the CexCandle client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.cex_candle import CexCandle
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_CANDLE = {"data": [{"d": "1700000000", "o": "100", "h": "110", "l": "90", "c": "105"}]}


def _client():
    return CexCandle(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/cex/candle", _CANDLE)
def test_candle_returns_dataframe():
    df = _client()(exchange="binance", market="spot", symbol="BTC-USDT")
    assert isinstance(df, pd.DataFrame)
    assert "c" in df.columns
    assert len(df) == 1


@responses.activate
def test_candle_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/candle.*"),
        json=_CANDLE,
        status=200,
    )
    _client()(exchange="binance", market="spot", symbol="BTC-USDT", interval="1h")
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["market"] == ["spot"]
    assert qs["symbol"] == ["BTC-USDT"]
    assert qs["interval"] == ["1h"]
    assert qs["currency"] == ["USD"]
    assert "from" not in qs and "to" not in qs


def test_candle_invalid_market_raises_value_error():
    with pytest.raises(ValueError):
        _client()(exchange="binance", market="bogus", symbol="BTC-USDT")


@mock_http_response(responses.GET, "/api/v1/cex/candle/exchanges", ["binance", "okx"])
def test_candle_exchanges_returns_list():
    assert _client().exchanges(market="spot") == ["binance", "okx"]


@mock_http_response(
    responses.GET, "/api/v1/cex/candle/symbols", [{"symbol": "BTC-USDT"}]
)
def test_candle_symbols_returns_list():
    res = _client().symbols(exchange="binance", market="spot")
    assert res == [{"symbol": "BTC-USDT"}]


@mock_http_response(responses.GET, "/api/v1/cex/candle/intervals", ["1m", "1h", "1d"])
def test_candle_intervals_returns_list():
    assert _client().intervals() == ["1m", "1h", "1d"]


@mock_http_response(
    responses.GET, "/api/v1/cex/candle", {"error": "bad request"}, http_status=400
)
def test_candle_client_error():
    with pytest.raises(ClientError):
        _client()(exchange="binance", market="spot", symbol="BTC-USDT")


@mock_http_response(
    responses.GET, "/api/v1/cex/candle", {"error": "boom"}, http_status=500
)
def test_candle_server_error():
    with pytest.raises(ServerError):
        _client()(exchange="binance", market="spot", symbol="BTC-USDT")
