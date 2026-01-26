"""
Unit tests for the base API class.

These tests verify the API class initialization and configuration.
They do not make actual API calls.
"""

import os
import requests
import pytest
from tests.util import random_str
from datamaxi.api import API
from datamaxi.__version__ import __version__
import logging


@pytest.fixture(autouse=True)
def clean_env():
    """Clear API key from environment before each test."""
    old_key = os.environ.pop("DATAMAXI_API_KEY", None)
    yield
    # Restore the key after the test
    if old_key is not None:
        os.environ["DATAMAXI_API_KEY"] = old_key


def test_API_initial():
    """Tests the API initialization without any parameters."""
    client = API()

    assert isinstance(client, API)
    assert client.api_key is None
    assert client.timeout == 10
    assert client.show_limit_usage is False
    assert client.show_header is False
    assert isinstance(client.session, requests.Session)
    assert (
        client.session.headers.get("Content-Type") == "application/json;charset=utf-8"
    )
    assert client.session.headers.get("User-Agent") == "datamaxi/" + __version__
    assert client.session.headers.get("X-DTMX-APIKEY") == "None"
    assert client._logger is logging.getLogger("datamaxi.api")


def test_API_env_key():
    """Tests the API initialization with API key in environment variable."""
    api_key = random_str()
    os.environ["DATAMAXI_API_KEY"] = api_key
    client = API()

    assert isinstance(client, API)
    assert client.api_key == api_key
    assert client.session.headers.get("X-DTMX-APIKEY") == api_key


def test_API_with_explicit_key():
    """Tests the API initialization with explicit API key parameter."""
    api_key = random_str()
    client = API(api_key)

    assert isinstance(client, API)
    assert client.api_key == api_key
    assert client.session.headers.get("X-DTMX-APIKEY") == api_key


def test_API_explicit_key_overrides_env():
    """Tests that explicit API key overrides environment variable."""
    env_key = random_str()
    explicit_key = random_str()
    os.environ["DATAMAXI_API_KEY"] = env_key
    client = API(explicit_key)

    assert client.api_key == explicit_key
    assert client.session.headers.get("X-DTMX-APIKEY") == explicit_key


def test_API_with_extra_parameters():
    """Tests the API initialization with extra parameters."""
    api_key = random_str()
    base_url = random_str()
    proxies = {"https": "https://1.2.3.4:8080"}

    client = API(
        api_key,
        base_url=base_url,
        show_limit_usage=True,
        show_header=True,
        timeout=0.1,
        proxies=proxies,
    )

    assert isinstance(client, API)
    assert client.api_key == api_key
    assert client.timeout == 0.1
    assert client.base_url == base_url
    assert client.show_limit_usage is True
    assert client.show_header is True
    assert client.proxies == proxies
    assert client.session.headers.get("X-DTMX-APIKEY") == api_key


def test_API_with_custom_timeout():
    """Tests the API initialization with custom timeout."""
    client = API(timeout=30)
    assert client.timeout == 30


def test_API_with_show_limit_usage():
    """Tests the API initialization with show_limit_usage enabled."""
    client = API(show_limit_usage=True)
    assert client.show_limit_usage is True


def test_API_with_show_header():
    """Tests the API initialization with show_header enabled."""
    client = API(show_header=True)
    assert client.show_header is True
