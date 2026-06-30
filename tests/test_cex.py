"""Local (mocked) tests for the Cex aggregator wiring. No API key / network."""

import responses

from datamaxi.datamaxi.cex import Cex
from datamaxi.datamaxi.cex_candle import CexCandle
from datamaxi.datamaxi.cex_ticker import CexTicker
from datamaxi.datamaxi.cex_fee import CexFee
from datamaxi.datamaxi.cex_wallet_status import CexWalletStatus
from datamaxi.datamaxi.cex_announcement import CexAnnouncement
from datamaxi.datamaxi.cex_token import CexToken
from datamaxi.datamaxi.cex_symbol import CexSymbol
from tests.util import mock_http_response

BASE_URL = "https://api.datamaxiplus.com"


def _client():
    return Cex(api_key="key", base_url=BASE_URL)


def test_cex_wires_subclients():
    cex = _client()
    assert isinstance(cex.candle, CexCandle)
    assert isinstance(cex.ticker, CexTicker)
    assert isinstance(cex.fee, CexFee)
    assert isinstance(cex.wallet_status, CexWalletStatus)
    assert isinstance(cex.announcement, CexAnnouncement)
    assert isinstance(cex.token, CexToken)
    assert isinstance(cex.symbol, CexSymbol)


@mock_http_response(responses.GET, "/api/v1/cex/candle/intervals", ["1m", "1h", "1d"])
def test_cex_candle_call_through_facade():
    assert _client().candle.intervals() == ["1m", "1h", "1d"]
