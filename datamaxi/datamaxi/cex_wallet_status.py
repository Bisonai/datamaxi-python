from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import check_required_parameter


class CexWalletStatus(API):
    """Client to fetch transfer status data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize wallet status client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def __call__(
        self,
        exchange: str,
        asset: str,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch transfer status data

        `GET /api/v1/wallet-status`

        <https://docs.datamaxiplus.com/rest/cex/wallet-status/data>

        Args:
            exchange (str): Exchange name
            asset (str): Asset name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Wallet status data
        """
        check_required_parameters(
            [
                [exchange, "exchange"],
                [asset, "asset"],
            ]
        )

        params = {
            "exchange": exchange,
            "asset": asset,
        }

        url_path = "/api/v1/wallet-status"
        res = self.query(url_path, params)
        if pandas:
            df = pd.DataFrame(res)
            df = df.set_index("network")
            return df

        return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.CexWalletStatus.__call__](./#datamaxi.datamaxi.CexWalletStatus.__call__)
        API.

        `GET /api/v1/wallet-status/exchanges`

        <https://docs.datamaxiplus.com/rest/cex/wallet-status/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/wallet-status/exchanges"
        return self.query(url_path)

    def assets(self, exchange: str) -> List[str]:
        """Fetch supported assets accepted by
        [datamaxi.CexWalletStatus.__call__](./#datamaxi.datamaxi.CexWalletStatus.__call__)
        API.

        `GET /api/v1/wallet-status/assets`

        <https://docs.datamaxiplus.com/rest/cex/wallet-status/assets>

        Args:
            exchange (str): Exchange name

        Returns:
            List of supported assets
        """
        check_required_parameter(exchange, "exchange")

        params = {
            "exchange": exchange,
        }

        url_path = "/api/v1/wallet-status/assets"
        return self.query(url_path, params)
