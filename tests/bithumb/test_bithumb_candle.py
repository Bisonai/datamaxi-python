import responses

from datamaxi.bithumb import Bithumb as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Timestamp",
        "OpenPrice",
        "ClosePrice",
        "HighPrice",
        "LowPrice",
        "Volume",
    ],
    [
        1609459200000,
        "28923.63000000",
        "29600.00000000",
        "28624.57000000",
        "29331.69000000",
        1314910,
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/bithumb/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_bithumb_candle():
    """Tests the API endpoint to get Bithumb candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
