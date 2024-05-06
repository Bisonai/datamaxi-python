import responses

from datamaxi.bybit import Bybit as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Timestamp",
        "OpenPrice",
        "HighPrice",
        "LowPrice",
        "ClosePrice",
        "Volume",
        "Turnover",
    ],
    [
        1638230400000,
        "57749.68",
        "59160.16",
        "55898.52",
        "56891.82",
        "993.599752",
        "56960429.11568562",
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/bybit/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_bybit_candle():
    """Tests the API endpoint to get Bybit candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
