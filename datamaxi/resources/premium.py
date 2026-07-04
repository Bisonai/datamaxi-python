from __future__ import annotations

from typing import Any, List, Union, Optional, TYPE_CHECKING
from datamaxi.api import Resource
from datamaxi.resources.responses import PremiumResponse
from datamaxi.lib.constants import Market, SortOrder

if TYPE_CHECKING:
    import pandas as pd


class Premium(Resource):
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
        source_exchange: Optional[str] = None,
        target_exchange: Optional[str] = None,
        asset: Optional[str] = None,
        source_quote: Optional[str] = None,
        target_quote: Optional[str] = None,
        sort: Optional[SortOrder] = None,
        key: Optional[str] = None,
        page: int = 1,
        limit: int = 100,
        currency: Optional[str] = None,
        conversion_base: Optional[str] = None,
        min_sv: Optional[str] = None,
        min_tv: Optional[str] = None,
        source_market: Optional[Market] = None,
        target_market: Optional[Market] = None,
        only_transferable: bool = False,
        network: Optional[str] = None,
        premium_type: Optional[str] = None,
        token_include: Optional[str] = None,
        token_exclude: Optional[str] = None,
        query: Optional[str] = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, PremiumResponse]:
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
            query (str): Search query for filtering assets

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

        if query is not None:
            params["query"] = query

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
            import pandas as pd

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
