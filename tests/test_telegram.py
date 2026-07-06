"""Local (mocked) tests for the Telegram client. No API key / network."""

import re
import responses
import pytest
from urllib.parse import urlparse, parse_qs

from datamaxi import Datamaxi, Telegram
from datamaxi.error import ClientError, ServerError
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"

_CHANNELS = {"data": [{"name": "alpha", "category": "news"}]}
_MESSAGES = {"data": [{"channel": "alpha", "text": "gm"}]}


def _client():
    return Telegram(api_key="key", base_url=BASE_URL)


def _qs(call):
    return parse_qs(urlparse(call.request.url).query)


@mock_http_response(responses.GET, "/api/v1/telegram/channels", _CHANNELS)
def test_channels_returns_response_and_next():
    res, next_request = _client().channels()
    assert res == _CHANNELS
    assert callable(next_request)


@responses.activate
def test_channels_sends_query_params():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/telegram/channels.*"),
        json=_CHANNELS,
        status=200,
    )
    _client().channels(page=2, limit=50, category="news")
    qs = _qs(responses.calls[0])
    assert qs["page"] == ["2"]
    assert qs["limit"] == ["50"]
    assert qs["sort"] == ["desc"]
    assert qs["category"] == ["news"]


@mock_http_response(responses.GET, "/api/v1/telegram/messages", _MESSAGES)
def test_messages_returns_response_and_next():
    res, next_request = _client().messages(channel_name="alpha")
    assert res == _MESSAGES
    assert callable(next_request)


@responses.activate
def test_messages_sends_channel_param():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/telegram/messages.*"),
        json=_MESSAGES,
        status=200,
    )
    _client().messages(channel_name="alpha")
    qs = _qs(responses.calls[0])
    assert qs["channel"] == ["alpha"]


@responses.activate
def test_messages_forwards_search_query():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/telegram/messages.*"),
        json=_MESSAGES,
        status=200,
    )
    _client().messages(channel_name="alpha", search_query="airdrop")
    qs = _qs(responses.calls[0])
    assert qs["search_query"] == ["airdrop"]


def test_channels_invalid_sort_raises_value_error():
    with pytest.raises(ValueError):
        _client().channels(sort="bogus")


@mock_http_response(
    responses.GET,
    "/api/v1/telegram/channels",
    {"error": "bad request"},
    http_status=400,
)
def test_channels_client_error():
    with pytest.raises(ClientError):
        _client().channels()


@mock_http_response(
    responses.GET, "/api/v1/telegram/messages", {"error": "boom"}, http_status=500
)
def test_messages_server_error():
    with pytest.raises(ServerError):
        _client().messages(channel_name="alpha")


# --- mounted sub-resource on Datamaxi (see #184) ---


def test_telegram_mounted_reuses_shared_session():
    maxi = Datamaxi(api_key="key", base_url=BASE_URL)
    assert isinstance(maxi.telegram, Telegram)
    # Same shared API/transport as every other sub-resource.
    assert maxi.telegram._api is maxi._api
    assert maxi.telegram._api is maxi.cex._api


@mock_http_response(responses.GET, "/api/v1/telegram/channels", _CHANNELS)
def test_telegram_mounted_channels_work():
    maxi = Datamaxi(api_key="key", base_url=BASE_URL)
    res, next_request = maxi.telegram.channels()
    assert res == _CHANNELS
    assert callable(next_request)


@mock_http_response(responses.GET, "/api/v1/telegram/messages", _MESSAGES)
def test_telegram_mounted_messages_work():
    maxi = Datamaxi(api_key="key", base_url=BASE_URL)
    res, next_request = maxi.telegram.messages(channel_name="alpha")
    assert res == _MESSAGES
    assert callable(next_request)
