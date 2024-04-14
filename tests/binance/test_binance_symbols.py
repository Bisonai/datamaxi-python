import responses

from datamaxi.binance import Binance as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = ["a", "b", "c"]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/raw/binance/symbols",
    mock_item,
    200,
)
def test_binance_symbols():
    """Tests the API endpoint to get Binance supported symbols"""

    response = client.symbols()
    response.should.equal(mock_item)
