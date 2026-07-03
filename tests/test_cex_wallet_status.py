"""Local (mocked) tests for the CexWalletStatus client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.resources.cex_wallet_status import CexWalletStatus
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_STATUS = [
    {"network": "BSC", "depositEnable": True, "withdrawEnable": True},
    {"network": "ETH", "depositEnable": False, "withdrawEnable": True},
]


def _client():
    return CexWalletStatus(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/wallet-status", _STATUS)
def test_wallet_status_returns_dataframe():
    df = _client()(exchange="binance", asset="BTC")
    assert isinstance(df, pd.DataFrame)
    assert df.index.name == "network"
    assert "depositEnable" in df.columns
    assert len(df) == 2


@mock_http_response(responses.GET, "/api/v1/wallet-status", _STATUS)
def test_wallet_status_pandas_false_returns_raw():
    res = _client()(exchange="binance", asset="BTC", pandas=False)
    assert res == _STATUS


@responses.activate
def test_wallet_status_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/wallet-status.*"),
        json=_STATUS,
        status=200,
    )
    _client()(exchange="binance", asset="BTC")
    qs = _qs(responses.calls[0])
    assert qs["exchange"] == ["binance"]
    assert qs["asset"] == ["BTC"]


@mock_http_response(
    responses.GET, "/api/v1/wallet-status/exchanges", ["binance", "okx"]
)
def test_wallet_status_exchanges_returns_list():
    assert _client().exchanges() == ["binance", "okx"]


@mock_http_response(responses.GET, "/api/v1/wallet-status/assets", ["BTC", "ETH"])
def test_wallet_status_assets_returns_list():
    assert _client().assets(exchange="binance") == ["BTC", "ETH"]


@mock_http_response(
    responses.GET, "/api/v1/wallet-status", {"error": "bad request"}, http_status=400
)
def test_wallet_status_client_error():
    with pytest.raises(ClientError):
        _client()(exchange="binance", asset="BTC")


@mock_http_response(
    responses.GET, "/api/v1/wallet-status", {"error": "boom"}, http_status=500
)
def test_wallet_status_server_error():
    with pytest.raises(ServerError):
        _client()(exchange="binance", asset="BTC")
