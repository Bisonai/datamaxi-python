"""
Quick smoke tests for DataMaxi+ API endpoints.

These tests perform basic API calls to verify endpoints work.
For comprehensive parameter testing, see test_integration.py.

Usage:
    export DATAMAXI_API_KEY="your_api_key"
    python -m pytest tests/test_call.py -v
"""

import os
import pytest
from datamaxi import Datamaxi, Telegram, Naver

# Skip all tests if no API key is provided
API_KEY = os.getenv("DATAMAXI_API_KEY") or os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"

pytestmark = pytest.mark.skipif(
    not API_KEY,
    reason="API key not provided. Set DATAMAXI_API_KEY environment variable.",
)


@pytest.fixture(scope="module")
def datamaxi():
    return Datamaxi(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def telegram():
    return Telegram(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def naver():
    return Naver(api_key=API_KEY, base_url=BASE_URL)


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


def test_funding_rate(datamaxi):
    """Smoke test for funding rate endpoints."""
    datamaxi.funding_rate.history(exchange="binance", symbol="BTC-USDT")
    datamaxi.funding_rate.latest(exchange="binance", symbol="BTC-USDT")
    datamaxi.funding_rate.exchanges()
    datamaxi.funding_rate.symbols(exchange="binance")


def test_dex(datamaxi):
    """Smoke test for DEX endpoints."""
    datamaxi.dex.chains()
    datamaxi.dex.exchanges()
    datamaxi.dex.pools(exchange="klayswap", chain="kaia_mainnet")
    datamaxi.dex.intervals()
    datamaxi.dex.trade(
        exchange="pancakeswap",
        chain="bsc_mainnet",
        pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
    )


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


def test_naver(naver):
    """Smoke test for naver endpoints."""
    naver.symbols()
    result = naver.trend("BTC")
    assert hasattr(result, "head")
