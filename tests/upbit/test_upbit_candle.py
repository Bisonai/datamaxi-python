import responses

from datamaxi.upbit import Upbit as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Timestamp",
        "OpenPrice",
        "HighPrice",
        "LowPrice",
        "TradePrice",
        "CandleAccTradePrice",
        "CandleAccTradeVolume",
    ],
    [
        1609459200000,
        "340.000000",
        "348.000000",
        "337.000000",
        "346.000000",
        "3000050607.793171",
        "8745870.599262",
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/upbit/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_upbit_candle():
    """Tests the API endpoint to get Upbit candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
