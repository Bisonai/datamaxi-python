import responses

from datamaxi.huobi import Huobi as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Timestamp",
        "OpenPrice",
        "ClosePrice",
        "LowPrice",
        "HighPrice",
        "Amount",
        "Volume",
        "Count",
    ],
    [
        1714752000000,
        "61688.750000",
        "62876.680000",
        "61537.530000",
        "63314.260000",
        "1297.564931",
        "80831210.618952",
        "100423",
    ],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/huobi/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_huobi_candle():
    """Tests the API endpoint to get Huobi candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
