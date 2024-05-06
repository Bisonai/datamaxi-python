import responses

from datamaxi.upbit import Upbit as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = ["a", "b", "c"]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/raw/upbit/intervals",
    mock_item,
    200,
)
def test_upbit_intervals():
    """Tests the API endpoint to get Upbit supported intervals"""

    response = client.intervals()
    response.should.equal(mock_item)
