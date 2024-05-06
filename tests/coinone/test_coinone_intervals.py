import responses

from datamaxi.coinone import Coinone as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = ["a", "b", "c"]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/raw/coinone/intervals",
    mock_item,
    200,
)
def test_coinone_intervals():
    """Tests the API endpoint to get Coinone supported intervals"""

    response = client.intervals()
    response.should.equal(mock_item)
