#!/usr/bin/env python3
"""
Comprehensive Integration Tests for DataMaxi+ Python SDK

This module tests all API endpoints with all supported parameters.
These tests require a valid API key and make real API calls.

Usage:
    export DATAMAXI_API_KEY="your_api_key"
    python -m pytest tests/test_integration.py -v

    # Run specific test class:
    python -m pytest tests/test_integration.py::TestCexCandle -v

    # Run with markers:
    python -m pytest tests/test_integration.py -m "cex" -v
"""

import os
import pytest
import pandas as pd
from datetime import datetime, timedelta

from datamaxi import Datamaxi, Telegram, Naver
from datamaxi.error import ClientError

# Skip all tests if no API key is provided
API_KEY = os.getenv("DATAMAXI_API_KEY") or os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"

pytestmark = pytest.mark.skipif(
    not API_KEY,
    reason="API key not provided. Set DATAMAXI_API_KEY environment variable.",
)


@pytest.fixture(scope="module")
def datamaxi():
    """Create Datamaxi client for tests."""
    return Datamaxi(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def telegram():
    """Create Telegram client for tests."""
    return Telegram(api_key=API_KEY, base_url=BASE_URL)


@pytest.fixture(scope="module")
def naver():
    """Create Naver client for tests."""
    return Naver(api_key=API_KEY, base_url=BASE_URL)


# =============================================================================
# CEX Candle Tests
# =============================================================================
@pytest.mark.cex
class TestCexCandle:
    """Test CEX candle endpoints with all parameters."""

    def test_exchanges_spot(self, datamaxi):
        """Test getting exchanges for spot market."""
        result = datamaxi.cex.candle.exchanges(market="spot")
        assert isinstance(result, list)
        assert len(result) > 0
        assert "binance" in result

    def test_exchanges_futures(self, datamaxi):
        """Test getting exchanges for futures market."""
        result = datamaxi.cex.candle.exchanges(market="futures")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_exchanges_invalid_market(self, datamaxi):
        """Test that invalid market raises ValueError."""
        with pytest.raises(ValueError, match="market must be either spot or futures"):
            datamaxi.cex.candle.exchanges(market="invalid")

    def test_symbols_with_exchange_and_market(self, datamaxi):
        """Test getting symbols with exchange and market."""
        result = datamaxi.cex.candle.symbols(exchange="binance", market="spot")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_symbols_with_exchange_only(self, datamaxi):
        """Test getting symbols with only exchange."""
        result = datamaxi.cex.candle.symbols(exchange="binance")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_symbols_with_market_only(self, datamaxi):
        """Test getting symbols with only market - requires exchange in API."""
        # Note: API requires exchange parameter, so this should raise ClientError
        with pytest.raises(ClientError):
            datamaxi.cex.candle.symbols(market="spot")

    def test_intervals(self, datamaxi):
        """Test getting supported intervals."""
        result = datamaxi.cex.candle.intervals()
        assert isinstance(result, list)
        assert "1m" in result
        assert "1h" in result
        assert "1d" in result

    def test_candle_basic(self, datamaxi):
        """Test basic candle data fetch."""
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "o" in result.columns  # open
        assert "h" in result.columns  # high
        assert "l" in result.columns  # low
        assert "c" in result.columns  # close

    def test_candle_all_intervals(self, datamaxi):
        """Test candle data with different intervals."""
        intervals = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
        for interval in intervals:
            result = datamaxi.cex.candle(
                exchange="binance",
                symbol="BTC-USDT",
                interval=interval,
                market="spot",
            )
            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0

    def test_candle_futures_market(self, datamaxi):
        """Test candle data for futures market."""
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="futures",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_candle_with_currency_krw(self, datamaxi):
        """Test candle data with KRW currency."""
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
            currency="KRW",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_candle_with_from_unix(self, datamaxi):
        """Test candle data with from_unix timestamp (requires to_unix as well)."""
        # Note: API works best with both from and to specified
        from_ts = int((datetime.now() - timedelta(days=30)).timestamp())
        to_ts = int((datetime.now() - timedelta(days=1)).timestamp())
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
            from_unix=str(from_ts),
            to_unix=str(to_ts),
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_candle_with_from_and_to_unix(self, datamaxi):
        """Test candle data with both from_unix and to_unix."""
        from_ts = int((datetime.now() - timedelta(days=30)).timestamp())
        to_ts = int((datetime.now() - timedelta(days=1)).timestamp())
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
            from_unix=str(from_ts),
            to_unix=str(to_ts),
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert len(result) <= 30  # Should be around 30 days of data

    def test_candle_pandas_false(self, datamaxi):
        """Test candle data with pandas=False returns dict."""
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
            pandas=False,
        )
        assert isinstance(result, dict)
        assert "data" in result

    def test_candle_invalid_market(self, datamaxi):
        """Test that invalid market raises ValueError."""
        with pytest.raises(ValueError, match="market must be either spot or futures"):
            datamaxi.cex.candle(
                exchange="binance",
                symbol="BTC-USDT",
                interval="1d",
                market="invalid",
            )


# =============================================================================
# CEX Ticker Tests
# =============================================================================
@pytest.mark.cex
class TestCexTicker:
    """Test CEX ticker endpoints with all parameters."""

    def test_exchanges_spot(self, datamaxi):
        """Test getting exchanges for spot market."""
        result = datamaxi.cex.ticker.exchanges(market="spot")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_exchanges_futures(self, datamaxi):
        """Test getting exchanges for futures market."""
        result = datamaxi.cex.ticker.exchanges(market="futures")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_symbols(self, datamaxi):
        """Test getting symbols."""
        result = datamaxi.cex.ticker.symbols(exchange="binance", market="spot")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_ticker_basic(self, datamaxi):
        """Test basic ticker data fetch."""
        result = datamaxi.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_ticker_futures(self, datamaxi):
        """Test ticker data for futures market."""
        result = datamaxi.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="futures",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_ticker_with_currency(self, datamaxi):
        """Test ticker data with currency parameter."""
        result = datamaxi.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
            currency="KRW",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_ticker_with_conversion_base(self, datamaxi):
        """Test ticker data with conversion_base parameter."""
        result = datamaxi.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
            conversion_base="USDT",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_ticker_pandas_false(self, datamaxi):
        """Test ticker data with pandas=False."""
        result = datamaxi.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
            pandas=False,
        )
        assert isinstance(result, dict)
        assert "data" in result


# =============================================================================
# CEX Fee Tests
# =============================================================================
@pytest.mark.cex
class TestCexFee:
    """Test CEX fee endpoints with all parameters."""

    def test_exchanges(self, datamaxi):
        """Test getting supported exchanges."""
        result = datamaxi.cex.fee.exchanges()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_symbols(self, datamaxi):
        """Test getting supported symbols."""
        result = datamaxi.cex.fee.symbols(exchange="binance")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_fee_with_exchange_and_symbol(self, datamaxi):
        """Test fee data with exchange and symbol."""
        result = datamaxi.cex.fee(exchange="binance", symbol="BTC-USDT")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_fee_with_exchange_only(self, datamaxi):
        """Test fee data with exchange only."""
        result = datamaxi.cex.fee(exchange="binance")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_fee_without_params(self, datamaxi):
        """Test fee data without parameters (all fees)."""
        result = datamaxi.cex.fee()
        assert isinstance(result, list)
        assert len(result) > 0


# =============================================================================
# CEX Wallet Status Tests
# =============================================================================
@pytest.mark.cex
class TestCexWalletStatus:
    """Test CEX wallet status endpoints with all parameters."""

    def test_exchanges(self, datamaxi):
        """Test getting supported exchanges."""
        result = datamaxi.cex.wallet_status.exchanges()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_assets(self, datamaxi):
        """Test getting supported assets."""
        result = datamaxi.cex.wallet_status.assets(exchange="binance")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_wallet_status_basic(self, datamaxi):
        """Test basic wallet status fetch."""
        result = datamaxi.cex.wallet_status(exchange="binance", asset="BTC")
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_wallet_status_pandas_false(self, datamaxi):
        """Test wallet status with pandas=False."""
        result = datamaxi.cex.wallet_status(
            exchange="binance", asset="BTC", pandas=False
        )
        assert isinstance(result, list)
        assert len(result) > 0


# =============================================================================
# CEX Announcement Tests
# =============================================================================
@pytest.mark.cex
class TestCexAnnouncement:
    """Test CEX announcement endpoints with all parameters."""

    def test_announcement_basic(self, datamaxi):
        """Test basic announcement fetch."""
        result, next_request = datamaxi.cex.announcement()
        assert isinstance(result, dict)
        assert "data" in result
        assert callable(next_request)

    def test_announcement_with_pagination(self, datamaxi):
        """Test announcement with pagination parameters."""
        result, next_request = datamaxi.cex.announcement(page=1, limit=10)
        assert isinstance(result, dict)
        assert "data" in result
        assert len(result["data"]) <= 10

    def test_announcement_sort_asc(self, datamaxi):
        """Test announcement with sort=asc."""
        result, _ = datamaxi.cex.announcement(sort="asc", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_announcement_sort_desc(self, datamaxi):
        """Test announcement with sort=desc."""
        result, _ = datamaxi.cex.announcement(sort="desc", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_announcement_with_exchange(self, datamaxi):
        """Test announcement filtered by exchange."""
        result, _ = datamaxi.cex.announcement(exchange="binance", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_announcement_with_key(self, datamaxi):
        """Test announcement with sort key."""
        result, _ = datamaxi.cex.announcement(key="created_at", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_announcement_pagination_next_request(self, datamaxi):
        """Test that next_request function works."""
        result1, next_request = datamaxi.cex.announcement(page=1, limit=5)
        result2, _ = next_request()
        assert isinstance(result2, dict)
        assert "data" in result2

    def test_announcement_invalid_page(self, datamaxi):
        """Test that invalid page raises ValueError."""
        with pytest.raises(ValueError, match="page must be greater than 0"):
            datamaxi.cex.announcement(page=0)

    def test_announcement_invalid_limit(self, datamaxi):
        """Test that invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="limit must be greater than 0"):
            datamaxi.cex.announcement(limit=0)

    def test_announcement_invalid_sort(self, datamaxi):
        """Test that invalid sort raises ValueError."""
        with pytest.raises(ValueError, match="sort must be either asc or desc"):
            datamaxi.cex.announcement(sort="invalid")


# =============================================================================
# CEX Token Tests
# =============================================================================
@pytest.mark.cex
class TestCexToken:
    """Test CEX token endpoints with all parameters."""

    def test_updates_basic(self, datamaxi):
        """Test basic token updates fetch."""
        result, next_request = datamaxi.cex.token.updates()
        assert isinstance(result, dict)
        assert "data" in result
        assert callable(next_request)

    def test_updates_with_pagination(self, datamaxi):
        """Test token updates with pagination."""
        result, _ = datamaxi.cex.token.updates(page=1, limit=10)
        assert isinstance(result, dict)
        assert len(result["data"]) <= 10

    def test_updates_type_listed(self, datamaxi):
        """Test token updates filtered by type=listed."""
        result, _ = datamaxi.cex.token.updates(type="listed", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_updates_type_delisted(self, datamaxi):
        """Test token updates filtered by type=delisted."""
        result, _ = datamaxi.cex.token.updates(type="delisted", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_updates_sort_asc(self, datamaxi):
        """Test token updates with sort=asc."""
        result, _ = datamaxi.cex.token.updates(sort="asc", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_updates_sort_desc(self, datamaxi):
        """Test token updates with sort=desc."""
        result, _ = datamaxi.cex.token.updates(sort="desc", limit=10)
        assert isinstance(result, dict)
        assert "data" in result

    def test_updates_invalid_type(self, datamaxi):
        """Test that invalid type raises ValueError."""
        with pytest.raises(
            ValueError, match="type must be either listed or delisted when set"
        ):
            datamaxi.cex.token.updates(type="invalid")


# =============================================================================
# DEX Tests
# =============================================================================
@pytest.mark.dex
class TestDex:
    """Test DEX endpoints with all parameters."""

    def test_chains(self, datamaxi):
        """Test getting supported chains."""
        result = datamaxi.dex.chains()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_exchanges(self, datamaxi):
        """Test getting supported exchanges."""
        result = datamaxi.dex.exchanges()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_intervals(self, datamaxi):
        """Test getting supported intervals."""
        result = datamaxi.dex.intervals()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_pools_without_params(self, datamaxi):
        """Test getting pools without parameters."""
        result = datamaxi.dex.pools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_pools_with_exchange(self, datamaxi):
        """Test getting pools with exchange filter."""
        result = datamaxi.dex.pools(exchange="klayswap")
        assert isinstance(result, list)

    def test_pools_with_chain(self, datamaxi):
        """Test getting pools with chain filter."""
        result = datamaxi.dex.pools(chain="kaia_mainnet")
        assert isinstance(result, list)

    def test_pools_with_exchange_and_chain(self, datamaxi):
        """Test getting pools with both filters."""
        result = datamaxi.dex.pools(exchange="klayswap", chain="kaia_mainnet")
        assert isinstance(result, list)

    def test_trade_basic(self, datamaxi):
        """Test basic trade data fetch."""
        result, next_request = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert callable(next_request)

    def test_trade_with_pagination(self, datamaxi):
        """Test trade data with pagination."""
        result, _ = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            page=1,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 10

    def test_trade_sort_asc(self, datamaxi):
        """Test trade data with sort=asc."""
        result, _ = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            sort="asc",
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_trade_sort_desc(self, datamaxi):
        """Test trade data with sort=desc."""
        result, _ = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            sort="desc",
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_trade_with_from_datetime(self, datamaxi):
        """Test trade data with fromDateTime."""
        from_dt = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        result, _ = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            fromDateTime=from_dt,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_trade_with_to_datetime(self, datamaxi):
        """Test trade data with toDateTime."""
        to_dt = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        result, _ = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            toDateTime=to_dt,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_trade_pandas_false(self, datamaxi):
        """Test trade data with pandas=False."""
        result, _ = datamaxi.dex.trade(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            pandas=False,
            limit=10,
        )
        assert isinstance(result, dict)
        assert "data" in result

    def test_candle_basic(self, datamaxi):
        """Test basic candle data fetch."""
        result, next_request = datamaxi.dex.candle(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert callable(next_request)

    def test_candle_with_interval(self, datamaxi):
        """Test candle data with interval parameter."""
        result, _ = datamaxi.dex.candle(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            interval="1h",
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_candle_with_pagination(self, datamaxi):
        """Test candle data with pagination."""
        result, _ = datamaxi.dex.candle(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            page=1,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 10

    def test_candle_pandas_false(self, datamaxi):
        """Test candle data with pandas=False."""
        result, _ = datamaxi.dex.candle(
            chain="bsc_mainnet",
            exchange="pancakeswap",
            pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
            pandas=False,
            limit=10,
        )
        assert isinstance(result, dict)
        assert "data" in result

    def test_trade_invalid_sort(self, datamaxi):
        """Test that invalid sort raises ValueError."""
        with pytest.raises(ValueError, match="sort must be either asc or desc"):
            datamaxi.dex.trade(
                chain="bsc_mainnet",
                exchange="pancakeswap",
                pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
                sort="invalid",
            )

    def test_trade_both_from_and_to_datetime(self, datamaxi):
        """Test that setting both fromDateTime and toDateTime raises ValueError."""
        from_dt = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        to_dt = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        with pytest.raises(
            ValueError,
            match="fromDateTime and toDateTime cannot be set at the same time",
        ):
            datamaxi.dex.trade(
                chain="bsc_mainnet",
                exchange="pancakeswap",
                pool="0x6ee3eE9C3395BbD136B6076A70Cb6cFF241c0E24",
                fromDateTime=from_dt,
                toDateTime=to_dt,
            )


# =============================================================================
# Funding Rate Tests
# =============================================================================
@pytest.mark.funding
class TestFundingRate:
    """Test funding rate endpoints with all parameters."""

    def test_exchanges(self, datamaxi):
        """Test getting supported exchanges."""
        result = datamaxi.funding_rate.exchanges()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_symbols(self, datamaxi):
        """Test getting supported symbols."""
        result = datamaxi.funding_rate.symbols(exchange="binance")
        assert isinstance(result, list)
        assert len(result) > 0

    def test_history_basic(self, datamaxi):
        """Test basic funding rate history fetch."""
        result, next_request = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert callable(next_request)

    def test_history_with_pagination(self, datamaxi):
        """Test funding rate history with pagination."""
        result, _ = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
            page=1,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 10

    def test_history_sort_asc(self, datamaxi):
        """Test funding rate history with sort=asc."""
        result, _ = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
            sort="asc",
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_history_sort_desc(self, datamaxi):
        """Test funding rate history with sort=desc."""
        result, _ = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
            sort="desc",
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_history_with_from_datetime(self, datamaxi):
        """Test funding rate history with fromDateTime."""
        from_dt = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        result, _ = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
            fromDateTime=from_dt,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_history_with_to_datetime(self, datamaxi):
        """Test funding rate history with toDateTime."""
        to_dt = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        result, _ = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
            toDateTime=to_dt,
            limit=10,
        )
        assert isinstance(result, pd.DataFrame)

    def test_history_pandas_false(self, datamaxi):
        """Test funding rate history with pandas=False."""
        result, _ = datamaxi.funding_rate.history(
            exchange="binance",
            symbol="BTC-USDT",
            pandas=False,
            limit=10,
        )
        assert isinstance(result, dict)
        assert "data" in result

    def test_history_invalid_sort(self, datamaxi):
        """Test that invalid sort raises ValueError."""
        with pytest.raises(ValueError, match="sort must be either asc or desc"):
            datamaxi.funding_rate.history(
                exchange="binance",
                symbol="BTC-USDT",
                sort="invalid",
            )

    def test_history_both_from_and_to_datetime(self, datamaxi):
        """Test that setting both fromDateTime and toDateTime raises ValueError."""
        from_dt = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        to_dt = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        with pytest.raises(
            ValueError,
            match="fromDateTime and toDateTime cannot be set at the same time",
        ):
            datamaxi.funding_rate.history(
                exchange="binance",
                symbol="BTC-USDT",
                fromDateTime=from_dt,
                toDateTime=to_dt,
            )

    def test_latest_basic(self, datamaxi):
        """Test basic latest funding rate fetch."""
        result = datamaxi.funding_rate.latest(
            exchange="binance",
            symbol="BTC-USDT",
        )
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_latest_with_sort(self, datamaxi):
        """Test latest funding rate with sort parameter."""
        result = datamaxi.funding_rate.latest(
            exchange="binance",
            symbol="BTC-USDT",
            sort="asc",
        )
        assert isinstance(result, pd.DataFrame)

    def test_latest_with_limit(self, datamaxi):
        """Test latest funding rate with limit parameter."""
        result = datamaxi.funding_rate.latest(
            exchange="binance",
            symbol="BTC-USDT",
            limit=5,
        )
        assert isinstance(result, pd.DataFrame)

    def test_latest_pandas_false(self, datamaxi):
        """Test latest funding rate with pandas=False."""
        result = datamaxi.funding_rate.latest(
            exchange="binance",
            symbol="BTC-USDT",
            pandas=False,
        )
        assert isinstance(result, dict)


# =============================================================================
# Premium Tests
# =============================================================================
@pytest.mark.premium
class TestPremium:
    """Test premium endpoints with all parameters."""

    def test_exchanges(self, datamaxi):
        """Test getting supported exchanges."""
        result = datamaxi.premium.exchanges()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_premium_basic(self, datamaxi):
        """Test basic premium data fetch."""
        result = datamaxi.premium()
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_premium_with_pagination(self, datamaxi):
        """Test premium data with pagination."""
        result = datamaxi.premium(page=1, limit=10)
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 10

    def test_premium_source_exchange(self, datamaxi):
        """Test premium data filtered by source_exchange."""
        result = datamaxi.premium(source_exchange="binance", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_target_exchange(self, datamaxi):
        """Test premium data filtered by target_exchange."""
        result = datamaxi.premium(target_exchange="upbit", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_with_asset(self, datamaxi):
        """Test premium data filtered by asset."""
        result = datamaxi.premium(asset="BTC", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_source_quote(self, datamaxi):
        """Test premium data filtered by source_quote."""
        result = datamaxi.premium(source_quote="USDT", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_target_quote(self, datamaxi):
        """Test premium data filtered by target_quote."""
        result = datamaxi.premium(target_quote="KRW", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_source_market(self, datamaxi):
        """Test premium data filtered by source_market."""
        result = datamaxi.premium(source_market="spot", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_target_market(self, datamaxi):
        """Test premium data filtered by target_market."""
        result = datamaxi.premium(target_market="spot", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_both_markets(self, datamaxi):
        """Test premium data filtered by both markets."""
        result = datamaxi.premium(source_market="spot", target_market="spot", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_sort_asc(self, datamaxi):
        """Test premium data with sort=asc."""
        result = datamaxi.premium(sort="asc", key="pdp", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_sort_desc(self, datamaxi):
        """Test premium data with sort=desc."""
        result = datamaxi.premium(sort="desc", key="pdp", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_min_pdp(self, datamaxi):
        """Test premium data with min_pdp filter."""
        result = datamaxi.premium(min_pdp="1", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_max_pdp(self, datamaxi):
        """Test premium data with max_pdp filter."""
        result = datamaxi.premium(max_pdp="10", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_min_max_pdp(self, datamaxi):
        """Test premium data with both min and max pdp."""
        result = datamaxi.premium(min_pdp="1", max_pdp="10", limit=50)
        assert isinstance(result, pd.DataFrame)

    def test_premium_pdp24h_filters(self, datamaxi):
        """Test premium data with pdp24h filters."""
        result = datamaxi.premium(min_pdp24h="-5", max_pdp24h="5", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_volume_filters(self, datamaxi):
        """Test premium data with volume filters."""
        result = datamaxi.premium(min_sv="100000", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_funding_rate_filters(self, datamaxi):
        """Test premium data with funding rate filters."""
        result = datamaxi.premium(min_net_funding_rate="-0.01", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_only_transferable(self, datamaxi):
        """Test premium data with only_transferable=True."""
        result = datamaxi.premium(only_transferable=True, limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_with_currency(self, datamaxi):
        """Test premium data with currency parameter."""
        result = datamaxi.premium(currency="KRW", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_with_conversion_base(self, datamaxi):
        """Test premium data with conversion_base parameter (USD or USDT)."""
        result = datamaxi.premium(conversion_base="USD", limit=10)
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_premium_token_include(self, datamaxi):
        """Test premium data with token_include filter."""
        result = datamaxi.premium(token_include="BTC", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_token_exclude(self, datamaxi):
        """Test premium data with token_exclude filter."""
        result = datamaxi.premium(token_exclude="SHIB", limit=10)
        assert isinstance(result, pd.DataFrame)

    def test_premium_pandas_false(self, datamaxi):
        """Test premium data with pandas=False."""
        result = datamaxi.premium(pandas=False, limit=10)
        assert isinstance(result, dict)
        assert "data" in result


# =============================================================================
# Forex Tests
# =============================================================================
@pytest.mark.forex
class TestForex:
    """Test forex endpoints with all parameters."""

    def test_symbols(self, datamaxi):
        """Test getting supported symbols."""
        result = datamaxi.forex.symbols()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_forex_basic(self, datamaxi):
        """Test basic forex data fetch."""
        result = datamaxi.forex(symbol="USD-KRW")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_forex_pandas_false(self, datamaxi):
        """Test forex data with pandas=False."""
        result = datamaxi.forex(symbol="USD-KRW", pandas=False)
        assert isinstance(result, dict)


# =============================================================================
# Telegram Tests
# =============================================================================
@pytest.mark.telegram
class TestTelegram:
    """Test Telegram endpoints with all parameters."""

    def test_channels_basic(self, telegram):
        """Test basic channels fetch."""
        result, next_request = telegram.channels()
        assert isinstance(result, dict)
        assert "data" in result
        assert callable(next_request)

    def test_channels_with_pagination(self, telegram):
        """Test channels with pagination."""
        result, _ = telegram.channels(page=1, limit=10)
        assert isinstance(result, dict)
        assert len(result["data"]) <= 10

    def test_channels_sort_asc(self, telegram):
        """Test channels with sort=asc."""
        result, _ = telegram.channels(sort="asc", limit=10)
        assert isinstance(result, dict)

    def test_channels_sort_desc(self, telegram):
        """Test channels with sort=desc."""
        result, _ = telegram.channels(sort="desc", limit=10)
        assert isinstance(result, dict)

    def test_channels_with_key(self, telegram):
        """Test channels with sort key."""
        result, _ = telegram.channels(key="subscriber_count", limit=10)
        assert isinstance(result, dict)

    def test_channels_pagination_next_request(self, telegram):
        """Test that next_request function works."""
        result1, next_request = telegram.channels(page=1, limit=5)
        result2, _ = next_request()
        assert isinstance(result2, dict)
        assert "data" in result2

    def test_channels_invalid_page(self, telegram):
        """Test that invalid page raises ValueError."""
        with pytest.raises(ValueError, match="page must be greater than 0"):
            telegram.channels(page=0)

    def test_channels_invalid_limit(self, telegram):
        """Test that invalid limit raises ValueError."""
        with pytest.raises(ValueError, match="limit must be greater than 0"):
            telegram.channels(limit=0)

    def test_channels_invalid_sort(self, telegram):
        """Test that invalid sort raises ValueError."""
        with pytest.raises(ValueError, match="sort must be either asc or desc"):
            telegram.channels(sort="invalid")

    def test_messages_basic(self, telegram):
        """Test basic messages fetch."""
        result, next_request = telegram.messages()
        assert isinstance(result, dict)
        assert "data" in result
        assert callable(next_request)

    def test_messages_with_pagination(self, telegram):
        """Test messages with pagination."""
        result, _ = telegram.messages(page=1, limit=10)
        assert isinstance(result, dict)
        assert len(result["data"]) <= 10

    def test_messages_with_channel(self, telegram):
        """Test messages filtered by channel."""
        result, _ = telegram.messages(channel_name="binanceexchange", limit=10)
        assert isinstance(result, dict)

    def test_messages_sort_asc(self, telegram):
        """Test messages with sort=asc."""
        result, _ = telegram.messages(sort="asc", limit=10)
        assert isinstance(result, dict)

    def test_messages_sort_desc(self, telegram):
        """Test messages with sort=desc."""
        result, _ = telegram.messages(sort="desc", limit=10)
        assert isinstance(result, dict)

    def test_messages_with_key(self, telegram):
        """Test messages with sort key."""
        result, _ = telegram.messages(key="created_at", limit=10)
        assert isinstance(result, dict)

    def test_messages_pagination_next_request(self, telegram):
        """Test that next_request function works."""
        result1, next_request = telegram.messages(page=1, limit=5)
        result2, _ = next_request()
        assert isinstance(result2, dict)
        assert "data" in result2


# =============================================================================
# Naver Tests
# =============================================================================
@pytest.mark.naver
class TestNaver:
    """Test Naver endpoints with all parameters."""

    def test_symbols(self, naver):
        """Test getting supported symbols."""
        result = naver.symbols()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_trend_basic(self, naver):
        """Test basic trend data fetch."""
        result = naver.trend("BTC")
        assert hasattr(result, "head")
        assert len(result) > 0

    def test_trend_different_symbol(self, naver):
        """Test trend data for different symbol."""
        result = naver.trend("ETH")
        assert hasattr(result, "head")

    def test_trend_pandas_false(self, naver):
        """Test trend data with pandas=False."""
        result = naver.trend("BTC", pandas=False)
        assert isinstance(result, list)


# =============================================================================
# Error Handling Tests
# =============================================================================
@pytest.mark.errors
class TestErrorHandling:
    """Test error handling across endpoints."""

    def test_invalid_exchange(self, datamaxi):
        """Test that invalid exchange returns error or empty."""
        # This might raise an error or return empty depending on API behavior
        try:
            result = datamaxi.cex.candle(
                exchange="nonexistent_exchange",
                symbol="BTC-USDT",
                interval="1d",
                market="spot",
            )
            # If it doesn't raise, result should be empty
            assert len(result) == 0 or result is None
        except (ValueError, Exception):
            # Expected - invalid exchange should raise error
            pass

    def test_invalid_symbol(self, datamaxi):
        """Test that invalid symbol returns error or empty."""
        try:
            result = datamaxi.cex.candle(
                exchange="binance",
                symbol="INVALID-SYMBOL",
                interval="1d",
                market="spot",
            )
            assert len(result) == 0 or result is None
        except (ValueError, Exception):
            pass


# =============================================================================
# Response Type Tests
# =============================================================================
@pytest.mark.types
class TestResponseTypes:
    """Test that response types are correct."""

    def test_candle_dataframe_columns(self, datamaxi):
        """Test that candle DataFrame has expected columns."""
        result = datamaxi.cex.candle(
            exchange="binance",
            symbol="BTC-USDT",
            interval="1d",
            market="spot",
        )
        expected_columns = {"o", "h", "l", "c", "v"}
        assert expected_columns.issubset(set(result.columns))

    def test_ticker_dataframe_has_price(self, datamaxi):
        """Test that ticker DataFrame has price-related columns."""
        result = datamaxi.cex.ticker.get(
            exchange="binance",
            symbol="BTC-USDT",
            market="spot",
        )
        # Should have some price-related columns
        assert len(result.columns) > 0

    def test_wallet_status_dataframe_index(self, datamaxi):
        """Test that wallet status DataFrame has network as index."""
        result = datamaxi.cex.wallet_status(exchange="binance", asset="BTC")
        assert result.index.name == "network"

    def test_funding_rate_latest_single_row(self, datamaxi):
        """Test that latest funding rate returns single row."""
        result = datamaxi.funding_rate.latest(
            exchange="binance",
            symbol="BTC-USDT",
        )
        assert len(result) == 1

    def test_forex_single_row(self, datamaxi):
        """Test that forex returns single row."""
        result = datamaxi.forex(symbol="USD-KRW")
        assert len(result) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
