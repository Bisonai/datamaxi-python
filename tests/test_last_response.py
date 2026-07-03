"""Local tests for last_response metadata + consistent (unwrapped) returns.

Covers #140: response metadata (rate-limit usage, headers, status) is exposed
via `client.<resource>.last_response` instead of being wrapped into the return
value, and the show_limit_usage/show_header flags no longer change the shape.
"""

import re
import responses
import pandas as pd

from datamaxi.resources.cex_ticker import CexTicker
from datamaxi.api import API, ResponseMeta

BASE_URL = "https://api.datamaxiplus.com"
_TICKER = {"data": {"d": "1700000000", "p": "105.5"}}
_RL_HEADERS = {
    "x-ratelimit-limit": "100",
    "x-ratelimit-remaining": "99",
    "x-ratelimit-reset": "60",
}


def _add_ticker(**extra):
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/ticker.*"),
        json=_TICKER,
        status=200,
        headers=_RL_HEADERS,
        **extra,
    )


def test_last_response_none_before_any_call():
    assert API(api_key="k", base_url=BASE_URL).last_response is None
    assert CexTicker(api_key="k", base_url=BASE_URL).last_response is None


@responses.activate
def test_last_response_populated_after_call():
    _add_ticker()
    c = CexTicker(api_key="k", base_url=BASE_URL)
    df = c.get(exchange="binance", market="spot", symbol="BTC-USDT")

    # return value is the payload (DataFrame), not a metadata wrapper
    assert isinstance(df, pd.DataFrame)

    lr = c.last_response
    assert isinstance(lr, ResponseMeta)
    assert lr.status_code == 200
    assert lr.data == _TICKER
    assert lr.limit_usage == {
        "x-ratelimit-limit": "100",
        "x-ratelimit-remaining": "99",
        "x-ratelimit-reset": "60",
    }
    assert lr.headers["x-ratelimit-remaining"] == "99"


@responses.activate
def test_flags_do_not_change_return_shape():
    _add_ticker()
    c = CexTicker(
        api_key="k", base_url=BASE_URL, show_limit_usage=True, show_header=True
    )
    df = c.get(exchange="binance", market="spot", symbol="BTC-USDT")
    # Previously these flags wrapped the return in a dict; now the shape is
    # identical to a plain client and metadata comes from last_response.
    assert isinstance(df, pd.DataFrame)
    assert c.last_response.limit_usage["x-ratelimit-limit"] == "100"


@responses.activate
def test_last_response_shared_across_client_tree():
    from datamaxi import Datamaxi

    _add_ticker()
    client = Datamaxi(api_key="k", base_url=BASE_URL)
    client.cex.ticker.get(exchange="binance", market="spot", symbol="BTC-USDT")
    # One shared transport (#137) -> last_response visible from any node
    assert client.cex.ticker.last_response.status_code == 200
    assert client.premium.last_response is client.cex.ticker.last_response
