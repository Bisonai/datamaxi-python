import responses

from datamaxi.binance import Binance as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Symbol",
        "OpenTime",
        "OpenPrice",
        "HighPrice",
        "LowPrice",
        "ClosePrice",
        "BaseVolume",
        "CloseTime",
        "QuoteVolume",
        "NumTrades",
        "TakerBuyVolume",
        "TakerBuyQuoteVolume",
    ],
    [
        "BTCUSDT",
        1609459200000,
        "28923.63000000",
        "29600.00000000",
        "28624.57000000",
        "29331.69000000",
        "54182.92501100",
        1609545599999,
        "1582526989.16187265",
        1314910,
        "27455.80172500",
        "802247744.54510409",
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/binance/kline\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_binance_kline():
    """Tests the API endpoint to get Binance trend."""

    response = client.kline(**params)
    response.should.equal(mock_item)
