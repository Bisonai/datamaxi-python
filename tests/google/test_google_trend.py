import responses

from datamaxi.google import Google as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [["Timestamp", "Ethereum"], ["2020-01-01 00:00", "9723"]]

key = random_str()
client = Client(key)

req_params = {"keyword": "Ethereum"}
params = {"keyword": "Ethereum", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/google/trend\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_google_trend():
    """Tests the API endpoint to get google trend."""

    response = client.trend(**params)
    response.should.equal(mock_item)
