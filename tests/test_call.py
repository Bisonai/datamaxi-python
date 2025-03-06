import os
import logging
from datamaxi import Datamaxi


logging.basicConfig(level=logging.INFO)

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL") or "https://api.datamaxiplus.com"

datamaxi = Datamaxi(api_key=api_key, base_url=base_url)


def testcall(func, **kwargs):
    name = f"{func.__module__}.{func.__qualname__}"
    logging.info(name)
    func(**kwargs)
    logging.info(f"{name} ok")


logging.info("cex candle")
testcall(
    datamaxi.cex.candle,
    exchange="binance",
    symbol="BTC-USDT",
    interval="1m",
    market="spot",
)
testcall(datamaxi.cex.candle.exchanges, market="spot")
testcall(datamaxi.cex.candle.symbols, exchange="binance", market="spot")
testcall(datamaxi.cex.candle.intervals)

logging.info("cex ticker")
testcall(datamaxi.cex.ticker.exchanges, market="spot")
testcall(datamaxi.cex.ticker.symbols, exchange="binance", market="spot")

logging.info("cex token updates")
testcall(datamaxi.cex.token.updates)

logging.info("cex fees")
testcall(datamaxi.cex.fee.get, exchange="binance", symbol="BTC-USDT")
testcall(datamaxi.cex.fee.exchanges)
testcall(datamaxi.cex.fee.symbols, exchange="binance")

logging.info("cex announcement")
testcall(datamaxi.cex.announcement.get)

logging.info("cex transfer")
testcall(datamaxi.cex.wallet_status.get, exchange="binance", asset="BTC")
testcall(datamaxi.cex.wallet_status.exchanges)
testcall(datamaxi.cex.wallet_status.assets, exchange="binance")

logging.info("funding rate")
testcall(datamaxi.funding_rate.history, exchange="binance", symbol="BTC-USDT")
testcall(datamaxi.funding_rate.latest, exchange="binance", symbol="BTC-USDT")
testcall(datamaxi.funding_rate.exchanges)
testcall(datamaxi.funding_rate.symbols, exchange="binance")


logging.info("dex")
testcall(datamaxi.dex.chains)
testcall(datamaxi.dex.exchanges)
testcall(datamaxi.dex.pools, exchange="klayswap", chain="kaia_mainnet")
testcall(datamaxi.dex.intervals)
testcall(
    datamaxi.dex.trade,
    exchange="pancakeswap",
    chain="bsc_mainnet",
    pool="0xb24cd29e32FaCDDf9e73831d5cD1FFcd1e535423",
)
testcall(
    datamaxi.dex.liquidity,
    exchange="pancakeswap",
    chain="bsc_mainnet",
    pool="0xb24cd29e32FaCDDf9e73831d5cD1FFcd1e535423",
)
testcall(
    datamaxi.dex.trade,
    exchange="pancakeswap",
    chain="bsc_mainnet",
    pool="0xb24cd29e32FaCDDf9e73831d5cD1FFcd1e535423",
)

logging.info("forex")
testcall(datamaxi.forex.symbols)
testcall(datamaxi.forex, symbol="USD-KRW", pandas=True)

logging.info("premium")
testcall(datamaxi.premium)
testcall(datamaxi.premium.exchanges)
