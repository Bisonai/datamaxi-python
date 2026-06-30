"""
Quick smoke tests for DataMaxi+ API endpoints.

These tests perform basic API calls to verify endpoints work.
For comprehensive parameter testing, see test_integration.py.

Usage:
    export DATAMAXI_API_KEY="your_api_key"
    python -m pytest tests/test_call.py -v
"""

import pytest

from tests.conftest import API_KEY, _FLAKY_PROD_DATA_XFAIL

# Live alive-check / smoke lane: a thin subset of test_integration.py that
# pings each endpoint once. Skipped without a key and deselected from the
# keyless CI lane via the `smoke` marker. Client fixtures and the
# flaky-prod-data marker come from tests/conftest.py.
pytestmark = [
    pytest.mark.smoke,
    pytest.mark.skipif(
        not API_KEY,
        reason="API key not provided. Set DATAMAXI_API_KEY environment variable.",
    ),
]


def test_cex_candle(datamaxi):
    """Smoke test for CEX candle endpoints."""
    datamaxi.cex.candle(
        exchange="binance",
        symbol="BTC-USDT",
        interval="1d",
        market="spot",
    )
    datamaxi.cex.candle.exchanges(market="spot")
    datamaxi.cex.candle.symbols(exchange="binance", market="spot")
    datamaxi.cex.candle.intervals()


def test_cex_ticker(datamaxi):
    """Smoke test for CEX ticker endpoints."""
    datamaxi.cex.ticker.get(exchange="binance", market="spot", symbol="BTC-USDT")
    datamaxi.cex.ticker.exchanges(market="spot")
    datamaxi.cex.ticker.symbols(exchange="binance", market="spot")


def test_cex_token_updates(datamaxi):
    """Smoke test for CEX token updates endpoint."""
    datamaxi.cex.token.updates()


def test_cex_fees(datamaxi):
    """Smoke test for CEX fee endpoints."""
    datamaxi.cex.fee(exchange="binance", symbol="BTC-USDT")
    datamaxi.cex.fee.exchanges()
    datamaxi.cex.fee.symbols(exchange="binance")


def test_cex_announcement(datamaxi):
    """Smoke test for CEX announcement endpoint."""
    datamaxi.cex.announcement()


def test_cex_wallet_status(datamaxi):
    """Smoke test for CEX wallet status endpoints."""
    datamaxi.cex.wallet_status(exchange="binance", asset="BTC")
    datamaxi.cex.wallet_status.exchanges()
    datamaxi.cex.wallet_status.assets(exchange="binance")


@_FLAKY_PROD_DATA_XFAIL
def test_funding_rate(datamaxi):
    """Smoke test for funding rate endpoints."""
    datamaxi.funding_rate.history(exchange="binance", symbol="BTC-USDT")
    datamaxi.funding_rate.latest(exchange="binance", symbol="BTC-USDT")
    datamaxi.funding_rate.exchanges()
    datamaxi.funding_rate.symbols(exchange="binance")


def test_forex(datamaxi):
    """Smoke test for forex endpoints."""
    datamaxi.forex.symbols()
    datamaxi.forex(symbol="USD-KRW")


def test_premium(datamaxi):
    """Smoke test for premium endpoints."""
    datamaxi.premium()
    datamaxi.premium.exchanges()


def test_telegram(telegram):
    """Smoke test for telegram endpoints."""
    telegram.channels()
    telegram.messages()


@_FLAKY_PROD_DATA_XFAIL
def test_naver(naver):
    """Smoke test for naver endpoints."""
    naver.symbols()
    result = naver.trend("BTC")
    assert hasattr(result, "head")
