"""Local (mocked) tests for the Naver client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi import Datamaxi
from datamaxi.naver import Naver
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_TREND = [{"d": "2024-01-01", "v": 10}, {"d": "2024-01-02", "v": 20}]


def _client():
    return Naver(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/naver-trend/symbols", ["BTC", "ETH"])
def test_naver_symbols_returns_list():
    assert _client().symbols() == ["BTC", "ETH"]


@mock_http_response(responses.GET, "/api/v1/naver-trend", _TREND)
def test_naver_trend_returns_dataframe():
    df = _client().trend("BTC")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "v" in df.columns


@mock_http_response(responses.GET, "/api/v1/naver-trend", _TREND)
def test_naver_trend_pandas_false_returns_raw():
    assert _client().trend("BTC", pandas=False) == _TREND


@responses.activate
def test_naver_trend_sends_symbol_query():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/naver-trend.*"),
        json=_TREND,
        status=200,
    )
    _client().trend("BTC")
    qs = _qs(responses.calls[0])
    assert qs["symbol"] == ["BTC"]


@mock_http_response(
    responses.GET, "/api/v1/naver-trend", {"error": "bad request"}, http_status=400
)
def test_naver_trend_client_error():
    with pytest.raises(ClientError):
        _client().trend("BTC")


@mock_http_response(
    responses.GET, "/api/v1/naver-trend", {"error": "boom"}, http_status=500
)
def test_naver_trend_server_error():
    with pytest.raises(ServerError):
        _client().trend("BTC")


def test_naver_mounted_reuses_shared_session():
    maxi = Datamaxi(api_key="key", base_url=BASE_URL)
    assert isinstance(maxi.naver, Naver)
    # Same shared API/transport as every other sub-resource.
    assert maxi.naver._api is maxi._api
    assert maxi.naver._api is maxi.cex._api


@mock_http_response(responses.GET, "/api/v1/naver-trend", _TREND)
def test_naver_mounted_trend_works():
    maxi = Datamaxi(api_key="key", base_url=BASE_URL)
    df = maxi.naver.trend("BTC")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_standalone_naver_not_top_level_importable():
    import datamaxi

    assert not hasattr(datamaxi, "Naver")
