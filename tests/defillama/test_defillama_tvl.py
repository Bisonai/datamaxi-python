import responses

from datamaxi.defillama import Defillama as Client
from tests.util import random_str
from tests.util import mock_http_response


mock_item = [
    ["Timestamp", "Usd"],
    ["03/30/2024 00:00:00", "97684389340.879684"],
]

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/defillama/tvl",
    mock_item,
    200,
)
def test_defillama_tvl():
    """Tests the API endpoint to get Defillama tvls."""

    response = client.tvl(pandas=False)
    response.should.equal(mock_item)
