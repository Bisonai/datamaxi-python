"""Local (mocked) tests for the CexAnnouncement client. No API key / network."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.cex_announcement import CexAnnouncement
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_ANNOUNCE = {"data": [{"title": "New listing", "exchange": "binance"}]}


def _client():
    return CexAnnouncement(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/cex/announcements", _ANNOUNCE)
def test_announcement_returns_response_and_next():
    res, next_request = _client()()
    assert res == _ANNOUNCE
    assert callable(next_request)


@responses.activate
def test_announcement_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/cex/announcements.*"),
        json=_ANNOUNCE,
        status=200,
    )
    _client()(page=2, limit=50, exchange="binance")
    qs = _qs(responses.calls[0])
    assert qs["page"] == ["2"]
    assert qs["limit"] == ["50"]
    assert qs["sort"] == ["desc"]
    assert qs["exchange"] == ["binance"]


def test_announcement_invalid_sort_raises_value_error():
    with pytest.raises(ValueError):
        _client()(sort="bogus")


def test_announcement_invalid_page_raises_value_error():
    with pytest.raises(ValueError):
        _client()(page=0)


@mock_http_response(
    responses.GET,
    "/api/v1/cex/announcements",
    {"error": "bad request"},
    http_status=400,
)
def test_announcement_client_error():
    with pytest.raises(ClientError):
        _client()()


@mock_http_response(
    responses.GET, "/api/v1/cex/announcements", {"error": "boom"}, http_status=500
)
def test_announcement_server_error():
    with pytest.raises(ServerError):
        _client()()
