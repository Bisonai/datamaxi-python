"""Local tests for the transient-5xx retry policy mounted on the session.

`responses` intercepts at the adapter-send level, which sits *above* urllib3's
Retry, so retries can't be exercised through it. These tests assert the retry
policy is wired onto the session adapters with the expected configuration.
"""

from datamaxi.api import API
from datamaxi import Datamaxi

BASE_URL = "https://api.datamaxiplus.com"


def _retry(client):
    return client.session.get_adapter(BASE_URL).max_retries


def test_default_retry_policy_mounted():
    r = _retry(API(api_key="k", base_url=BASE_URL))
    assert r.total == 3
    assert tuple(r.status_forcelist) == (502, 503, 504)
    assert r.backoff_factor == 0.5
    assert r.respect_retry_after_header is True
    assert r.raise_on_status is False
    assert "GET" in r.allowed_methods
    assert "POST" not in r.allowed_methods


def test_retries_disabled_when_zero():
    r = _retry(API(api_key="k", base_url=BASE_URL, max_retries=0))
    assert r.total == 0


def test_retry_params_are_tunable():
    r = _retry(
        API(
            api_key="k",
            base_url=BASE_URL,
            max_retries=5,
            retry_backoff=1.5,
            retry_statuses=(500, 502),
        )
    )
    assert r.total == 5
    assert r.backoff_factor == 1.5
    assert tuple(r.status_forcelist) == (500, 502)


def test_same_adapter_mounted_for_http_and_https():
    client = API(api_key="k", base_url=BASE_URL)
    assert client.session.get_adapter("https://x") is client.session.get_adapter(
        "http://x"
    )


def test_retry_config_propagates_through_datamaxi():
    c = Datamaxi(api_key="k", max_retries=7)
    # The whole tree shares one API/session (see #137), so the policy is shared.
    assert _retry(c.cex._api).total == 7
    assert _retry(c.premium._api).total == 7
