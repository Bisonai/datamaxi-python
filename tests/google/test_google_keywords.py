import responses

from datamaxi.google import Google as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = ["a", "b", "c"]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/google/keywords",
    mock_item,
    200,
)
def test_google_keywords():
    """Tests the API endpoint to get google trend keywords."""

    response = client.keywords()
    response.should.equal(mock_item)
