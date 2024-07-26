from typing import Any, List, Dict, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameters


class Premium(API):
    """Client to fetch premium data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize premium client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def get(
        self,
        sourceExchange: str,
        targetExchange: str,
        symbol: str,
        pandas: bool = True,
    ) -> Union[Dict, pd.DataFrame]:
        """Fetch premium data

        `GET /api/v1/premium`

        <https://docs.datamaxiplus.com/api/datasets/premium/premium>

        Args:
            sourceExchange (str): Source exchange name
            targetExchange (str): Target exchange name
            symbol (str): Symbol name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Premium data in pandas DataFrame
        """

        check_required_parameters(
            [
                [sourceExchange, "sourceExchange"],
                [targetExchange, "targetExchange"],
                [symbol, "symbol"],
            ]
        )

        params = {
            "sourceExchange": sourceExchange,
            "targetExchange": targetExchange,
            "symbol": symbol,
        }

        res = self.query("/api/v1/premium", params)

        if pandas:
            df = pd.DataFrame(res)
            df = df.set_index("d")
            return df
        else:
            return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.Premium.get](./#datamaxi.datamaxi.Premium.get)
        API.

        `GET /api/v1/Premium/exchanges`

        <https://docs.datamaxiplus.com/api/datasets/Premium/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/premium/exchanges"
        return self.query(url_path)

    def symbols(self, sourceExchange: str, targetExchange: str) -> List[str]:
        """Fetch supported symbols accepted by
        [datamaxi.Premium.get](./#datamaxi.datamaxi.Premium.get)
        API.

        `GET /api/v1/premium/symbols`

        <https://docs.datamaxiplus.com/api/datasets/premium/symbols>

        Args:
            sourceExchange (str): Source exchange name
            targetExchange (str): Target exchange name

        Returns:
            List of supported symbols
        """
        check_required_parameters(
            [
                [sourceExchange, "sourceExchange"],
                [targetExchange, "targetExchange"],
            ]
        )

        params = {"sourceExchange": sourceExchange, "targetExchange": targetExchange}

        url_path = "/api/v1/premium/symbols"
        return self.query(url_path, params)
