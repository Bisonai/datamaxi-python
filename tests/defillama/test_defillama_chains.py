import responses

from datamaxi.defillama import Defillama as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = ["a", "b", "c"]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/defillama/chain",
    mock_item,
    200,
)
def test_defillama_chains():
    """Tests the API endpoint to get Defillama chains."""

    response = client.chains()
    response.should.equal(mock_item)
