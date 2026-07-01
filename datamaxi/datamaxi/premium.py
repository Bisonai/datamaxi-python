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
        conversion_base: str = None,
        min_sv: str = None,
        min_tv: str = None,
        source_market: str = None,
        target_market: str = None,
        only_transferable: bool = False,
        network: str = None,
        premium_type: str = None,
        token_include: str = None,
        token_exclude: str = None,
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
            sort (str): Sort data by `asc` or `desc`
            key (str): Key to sort data
            page (int): Page number
            limit (int): Page size
            currency (str): Currency applied to cross-exchange price differences
            conversion_base (str): conversion base for price difference calculation
            min_sv (str): Return results with 24h volume in fiat on source exchange above min_sv
            min_tv (str): Return results with 24h volume in fiat on target exchange above min_tv
            source_market (str): Return results matching source market
            target_market (str): Return results matching target market
            only_transferable (bool): Return only transferable if set true
            network (str): Return results containing only specified network
            premium_type (str): Return based on matching premium_type
            token_include (str): Return results containing only specified token
            token_exclude (str): Return results not containing specified token

            pandas (bool): Return data as pandas DataFrame

        Returns:
            Premium data in pandas DataFrame
        """
        params = {}

        if source_exchange is not None:
            params["source_exchange"] = source_exchange

        if target_exchange is not None:
            params["target_exchange"] = target_exchange

        if asset is not None:
            params["asset"] = asset

        if source_quote is not None:
            params["source_quote"] = source_quote

        if target_quote is not None:
            params["target_quote"] = target_quote

        if sort is not None:
            params["sort"] = sort

        if key is not None:
            params["key"] = key

        if page is not None:
            params["page"] = page

        if limit is not None:
            params["limit"] = limit

        if currency is not None:
            params["currency"] = currency

        if conversion_base is not None:
            params["conversion_base"] = conversion_base

        if min_sv is not None:
            params["min_sv"] = min_sv

        if min_tv is not None:
            params["min_tv"] = min_tv

        if source_market is not None:
            params["source_market"] = source_market

        if target_market is not None:
            params["target_market"] = target_market

        if only_transferable:
            params["only_transferable"] = True

        if network is not None:
            params["network"] = network

        if premium_type is not None:
            params["premium_type"] = premium_type

        if token_include is not None:
            params["token_include"] = token_include

        if token_exclude is not None:
            params["token_exclude"] = token_exclude

        res = self.request_endpoint("premium", **params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        if pandas:
            df = pd.DataFrame(
                [
                    {
                        **item["detail"],
                        "source_annualized_funding_rate": item.get(
                            "source_annualized_funding_rate"
                        ),
                        "target_annualized_funding_rate": item.get(
                            "target_annualized_funding_rate"
                        ),
                    }
                    for item in res["data"]
                ]
            )
            return df
        else:
            return res

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges for premium data.

        `GET /api/v1/premium/exchanges`

        <https://docs.datamaxiplus.com/rest/premium/exchanges>

        Returns:
            List of supported exchanges
        """
        return self.request_endpoint("premium_exchanges")
