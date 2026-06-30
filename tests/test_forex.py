"""Local (mocked) tests for the Forex client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.forex import Forex
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"


def _client():
    return Forex(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(
    responses.GET, "/api/v1/forex", {"symbol": "USD-KRW", "price": "1380.5"}
)
def test_forex_call_returns_dataframe():
    df = _client()(symbol="USD-KRW")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["symbol"] == "USD-KRW"


@mock_http_response(
    responses.GET, "/api/v1/forex", {"symbol": "USD-KRW", "price": "1380.5"}
)
def test_forex_call_pandas_false_returns_dict():
    res = _client()(symbol="USD-KRW", pandas=False)
    assert isinstance(res, dict)
    assert res["symbol"] == "USD-KRW"


@responses.activate
def test_forex_call_sends_symbol_query():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/forex.*"),
        json={"symbol": "USD-KRW"},
        status=200,
    )
    _client()(symbol="USD-KRW")
    qs = _qs(responses.calls[0])
    assert qs["symbol"] == ["USD-KRW"]


@mock_http_response(responses.GET, "/api/v1/forex/symbols", ["USD-KRW", "EUR-USD"])
def test_forex_symbols_returns_list():
    res = _client().symbols()
    assert res == ["USD-KRW", "EUR-USD"]


@mock_http_response(
    responses.GET, "/api/v1/forex", {"error": "bad request"}, http_status=400
)
def test_forex_client_error():
    with pytest.raises(ClientError):
        _client()(symbol="USD-KRW")


@mock_http_response(responses.GET, "/api/v1/forex", {"error": "boom"}, http_status=500)
def test_forex_server_error():
    with pytest.raises(ServerError):
        _client()(symbol="USD-KRW")
