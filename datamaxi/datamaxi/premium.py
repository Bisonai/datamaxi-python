from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API


class Premium(API):
    """Client to fetch premium data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize premium client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

        self.__module__ = __name__
        self.__qualname__ = self.__class__.__qualname__

    def __call__(
        self,
        sourceExchange: str = None,
        targetExchange: str = None,
        asset: str = None,
        sourceQuote: str = None,
        targetQuote: str = None,
        currency: str = None,
        sort: str = None,
        limit: int = None,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Fetch premium data

        `GET /api/v1/premium`
        <https://docs.datamaxiplus.com/rest/premium/premium>

        Args:
            sourceExchange (str): Source exchange name
            targetExchange (str): Target exchange name
            asset (str): Asset name
            sourceQuote (str): Source quote currency
            targetQuote (str): Target quote currency
            currency (str): Currency applied to cross-exchange price differences
            sort (str): Sort data by `asc` or `desc`
            limit (int): Limit number of data to return
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Premium data in pandas DataFrame
        """
        params = {}

        if sort is not None:
            params["sort"] = sort

        if limit is not None:
            params["limit"] = limit

        if symbol is not None:
            params["symbol"] = symbol

        if sourceExchange is not None:
            params["sourceExchange"] = sourceExchange

        if targetExchange is not None:
            params["targetExchange"] = targetExchange

        if asset is not None:
            params["asset"] = asset

        if sourceQuote is not None:
            params["sourceQuote"] = sourceQuote

        if targetQuote is not None:
            params["targetQuote"] = targetQuote

        if currency is not None:
            params["currency"] = currency

        res = self.query("/api/v1/premium", params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        if pandas:
            df = pd.DataFrame(res["data"])
            df = df.set_index("d")
            return df
        else:
            return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.Premium.get](./#datamaxi.datamaxi.Premium.get)
        API.

        `GET /api/v1/Premium/exchanges`

        <https://docs.datamaxiplus.com/rest/Premium/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/premium/exchanges"
        return self.query(url_path)
