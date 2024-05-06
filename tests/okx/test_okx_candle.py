import responses

from datamaxi.okx import Okx as Client
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
        "VolumeCurrency",
        "VolumeCurrencyQuote",
    ],
    [
        1714694400000,
        "59062.2",
        "63349.9",
        "58800",
        "62875.9",
        "14714.37919201",
        "898204510.99459367",
        "898204510.99459367",
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/okx/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_okx_candle():
    """Tests the API endpoint to get Okx candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
