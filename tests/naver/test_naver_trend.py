import responses

from datamaxi.naver import Naver as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [["Date", "Ethereum"], ["2020-01-01 00:00", "9723"]]

key = random_str()
client = Client(key)

req_params = {"symbol": "ETH"}
params = {"symbol": "ETH", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/naver/trend\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_naver_trend():
    """Tests the API endpoint to get naver trend."""

    response = client.trend(**params)
    response.should.equal(mock_item)
