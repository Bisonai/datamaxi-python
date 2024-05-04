import responses

from datamaxi.coinone import Coinone as Client
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
        "TargetVolume",
        "QuoteVolume",
    ],
    [
        1709164800000,
        "87585000.0",
        "89380000.0",
        "85008000.0",
        "85787000.0",
        "932.51985118",
        "81067337869.2636",
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/coinone/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_coinone_candle():
    """Tests the API endpoint to get Coinone candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
