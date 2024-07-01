import responses

from datamaxi.gateio import Gateio as Client
from tests.util import random_str
from tests.util import mock_http_response
from urllib.parse import urlencode


mock_item = [
    [
        "Timestamp",
        "OpenPrice",
        "HighPrice",
        "LowPrice",
        "ClosePrice",
        "TradingVolumeInQuoteCurrency",
        "TradingVolumeInBaseCurrency"
  ],
  [
        1714752000000,
        "61693.2",
        "61693.2",
        "61681.2",
        "61681.3",
        "13176.79679900",
        "0.21360000"
  ],

]

key = random_str()
client = Client(key)

req_params = {"symbol": "BTC-USDT", "interval": "1d"}
params = {"symbol": "BTC-USDT", "interval": "1d", "pandas": False}


@mock_http_response(
    responses.GET,
    "/v1/raw/gateio/candle\\?" + urlencode(req_params),
    mock_item,
    200,
)
def test_gateio_candle():
    """Tests the API endpoint to get Gateio candle."""

    response = client.candle(**params)
    response.should.equal(mock_item)
