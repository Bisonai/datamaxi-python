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

    def __call__(  # noqa: C901
        self,
        source_exchange: str = None,
        target_exchange: str = None,
        asset: str = None,
        source_quote: str = None,
        target_quote: str = None,
        sort: str = None,
        key: str = None,
        page: int = 1,
        limit: int = 100,
        currency: str = None,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Fetch premium data

        `GET /api/v1/premium`
        <https://docs.datamaxiplus.com/rest/premium/premium>

        Args:
            source_exchange (str): Source exchange name
            target_exchange (str): Target exchange name
            asset (str): Asset name
            source_quote (str): Source quote currency
            target_quote (str): Target quote currency
            currency (str): Currency applied to cross-exchange price differences
            sort (str): Sort data by `asc` or `desc`
            key (str): Key to sort data
            page (int): Page number
            limit (int): Page size
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Premium data in pandas DataFrame
        """
        params = {}

        if source_exchange is not None:
            params["sourceExchange"] = source_exchange

        if target_exchange is not None:
            params["targetExchange"] = target_exchange

        if asset is not None:
            params["asset"] = asset

        if source_quote is not None:
            params["sourceQuote"] = source_quote

        if target_quote is not None:
            params["targetQuote"] = target_quote

        if sort is not None:
            params["sort"] = sort

        if page is not None:
            params["page"] = page

        if key is not None:
            params["key"] = key

        if limit is not None:
            params["limit"] = limit

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
