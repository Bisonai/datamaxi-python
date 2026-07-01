"""Local (mocked) tests for the CexToken client. No API key / network."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.cex_token import CexToken
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_UPDATES = {"data": [{"token": "BTC", "type": "listed"}]}


def _client():
    return CexToken(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/cex/token/updates", _UPDATES)
def test_token_updates_returns_response_and_next():
    res, next_request = _client().updates()
    assert res == _UPDATES
    assert callable(next_request)


@responses.activate
def test_token_updates_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/token/updates.*"),
        json=_UPDATES,
        status=200,
    )
    _client().updates(page=3, limit=10, type="listed")
    qs = _qs(responses.calls[0])
    assert qs["page"] == ["3"]
    assert qs["limit"] == ["10"]
    assert qs["type"] == ["listed"]


def test_token_updates_invalid_type_raises_value_error():
    with pytest.raises(ValueError):
        _client().updates(type="bogus")


@mock_http_response(
    responses.GET,
    "/api/v1/cex/token/updates",
    {"error": "bad request"},
    http_status=400,
)
def test_token_updates_client_error():
    with pytest.raises(ClientError):
        _client().updates()


@mock_http_response(
    responses.GET, "/api/v1/cex/token/updates", {"error": "boom"}, http_status=500
)
def test_token_updates_server_error():
    with pytest.raises(ServerError):
        _client().updates()
