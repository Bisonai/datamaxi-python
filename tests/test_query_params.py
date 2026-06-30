"""
Offline unit tests asserting the wire query-string keys for snake_case
public params (top_n / min_volume_usd).

Backend migrated these public params to snake_case canonical (dual-read).
These tests pin that the SDK sends the snake_case keys on the wire, and
that the user-facing ``topN`` kwarg stays accepted (non-breaking).
"""

import re
import responses
from urllib.parse import urlparse, parse_qs

from datamaxi.datamaxi.liquidation import Liquidation
from datamaxi.datamaxi.open_interest import OpenInterest

BASE_URL = "https://api.datamaxiplus.com"


def _query_of(call):
    return parse_qs(urlparse(call.request.url).query)


@responses.activate
def test_liquidation_heatmap_sends_top_n():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/liquidation/heatmap.*"),
        json={},
        status=200,
    )
    Liquidation(api_key="k", base_url=BASE_URL).heatmap(window="4h", topN=5)

    qs = _query_of(responses.calls[0])
    assert qs["top_n"] == ["5"]
    assert "topN" not in qs


@responses.activate
def test_open_interest_summary_sends_top_n():
    responses.add(
        responses.GET,
        re.compile(".*/api/v1/open-interest/summary.*"),
        json={},
        status=200,
    )
    OpenInterest(api_key="k", base_url=BASE_URL).summary(topN=7)

    qs = _query_of(responses.calls[0])
    assert qs["top_n"] == ["7"]
    assert "topN" not in qs
