import os
import logging
from datamaxi import Datamaxi


logging.basicConfig(level=logging.INFO)

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"

datamaxi = Datamaxi(api_key=api_key, base_url=base_url)


def test_cex_candle():
    datamaxi.cex.candle(
        exchange="binance",
        symbol="BTC-USDT",
        interval="1m",
        market="spot",
    )
    datamaxi.cex.candle.exchanges(market="spot")
    datamaxi.cex.candle.symbols(exchange="binance", market="spot")
    datamaxi.cex.candle.intervals()


def test_cex_ticker():
    datamaxi.cex.ticker.exchanges(market="spot")
    datamaxi.cex.ticker.symbols(exchange="binance", market="spot")


def test_cex_token_updates():
    datamaxi.cex.token.updates()


def test_cex_fees():
    datamaxi.cex.fee(exchange="binance", symbol="BTC-USDT")
    datamaxi.cex.fee.exchanges()
    datamaxi.cex.fee.symbols(exchange="binance")


def test_cex_announcement():
    datamaxi.cex.announcement()


def test_cex_wallet_status():
    datamaxi.cex.wallet_status(exchange="binance", asset="BTC")
    datamaxi.cex.wallet_status.exchanges()
    datamaxi.cex.wallet_status.assets(exchange="binance")


def test_test_funding_rate():
    datamaxi.funding_rate.history(exchange="binance", symbol="BTC-USDT")
    datamaxi.funding_rate.latest(exchange="binance", symbol="BTC-USDT")
    datamaxi.funding_rate.exchanges()
    datamaxi.funding_rate.symbols(exchange="binance")


def test_dex():
    datamaxi.dex.chains()
    datamaxi.dex.exchanges()
    datamaxi.dex.pools(exchange="klayswap", chain="kaia_mainnet")
    datamaxi.dex.intervals()
    datamaxi.dex.trade(
        exchange="pancakeswap",
        chain="bsc_mainnet",
        pool="0xb24cd29e32FaCDDf9e73831d5cD1FFcd1e535423",
    )
    datamaxi.dex.liquidity(
        exchange="pancakeswap",
        chain="bsc_mainnet",
        pool="0xb24cd29e32FaCDDf9e73831d5cD1FFcd1e535423",
    )
    datamaxi.dex.trade(
        exchange="pancakeswap",
        chain="bsc_mainnet",
        pool="0xb24cd29e32FaCDDf9e73831d5cD1FFcd1e535423",
    )


def test_forex():
    datamaxi.forex.symbols()
    datamaxi.forex(symbol="USD-KRW")


def test_premium():
    datamaxi.premium()
    datamaxi.premium.exchanges()
