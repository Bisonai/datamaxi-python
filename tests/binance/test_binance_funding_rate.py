import responses

from datamaxi.binance import Binance as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Date",
        "Funding Rate",
        "Mark Price",
    ],
    ["07/03/2024 16:00:00", "0.00010000", "60178.96865957"],
]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT"}
params = {"symbol": "BTC-USDT", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/binance/funding-rate\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_binance_funding_rate():
    """Tests the API endpoint to get Binance funding rate."""

    response = client.funding_rate(**params)
    response.should.equal(mock_item)
