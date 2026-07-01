"""Local (mocked) tests for the Premium client. No API key / network."""

import re
import responses
import pandas as pd
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.premium import Premium
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_RESPONSE = {
    "data": [
        {
            "detail": {"asset": "BTC", "pdp": "1.5"},
            "source_annualized_funding_rate": "0.1",
            "target_annualized_funding_rate": "0.2",
        }
    ]
}


def _client():
    return Premium(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/premium", _RESPONSE)
def test_premium_call_returns_dataframe():
    df = _client()()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["asset"] == "BTC"
    assert "source_annualized_funding_rate" in df.columns


@mock_http_response(responses.GET, "/api/v1/premium", _RESPONSE)
def test_premium_call_pandas_false_returns_raw():
    res = _client()(pandas=False)
    assert isinstance(res, dict)
    assert res["data"][0]["detail"]["asset"] == "BTC"


@responses.activate
def test_premium_call_param_name_translation():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/premium.*"),
        json=_RESPONSE,
        status=200,
    )
    _client()(
        source_exchange="binance",
        target_quote="USDT",
        conversion_base="USDT",
        page=2,
    )
    qs = _qs(responses.calls[0])
    # snake_case wire keys for all params (backend expects snake_case)
    assert qs["source_exchange"] == ["binance"]
    assert qs["target_quote"] == ["USDT"]
    assert qs["conversion_base"] == ["USDT"]
    assert qs["page"] == ["2"]


@mock_http_response(responses.GET, "/api/v1/premium/exchanges", ["binance", "upbit"])
def test_premium_exchanges_returns_list():
    assert _client().exchanges() == ["binance", "upbit"]


@mock_http_response(
    responses.GET, "/api/v1/premium", {"error": "bad request"}, http_status=400
)
def test_premium_client_error():
    with pytest.raises(ClientError):
        _client()()


@mock_http_response(
    responses.GET, "/api/v1/premium", {"error": "boom"}, http_status=500
)
def test_premium_server_error():
    with pytest.raises(ServerError):
        _client()()
