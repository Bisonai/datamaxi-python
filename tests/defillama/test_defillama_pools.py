import responses

from datamaxi.defillama import Defillama as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = ["a", "b", "c"]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/defillama/pool",
    mock_item,
    200,
)
def test_defillama_pools():
    """Tests the API endpoint to get Defillama pools."""

    response = client.pools()
    response.should.equal(mock_item)
