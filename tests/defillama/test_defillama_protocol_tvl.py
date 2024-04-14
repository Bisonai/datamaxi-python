import responses

from datamaxi.defillama import Defillama as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    ["Timestamp", "aave"],
    ["03/30/2024 00:00:00", "11349748481.861477"],
]

req_params = {"protocols": '["aave"]'}
params = {"protocols": "aave", "pandas": False}

key = random_str()
client = Client(key)


@mock_http_response(
    responses.GET,
    "/v1/defillama/tvl\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_defillama_protocol_tvl():
    """Tests the API endpoint to get Defillama protocol TVL."""

    response = client.protocol_tvl(**params)
    response.should.equal(mock_item)
