from __future__ import annotations

from typing import Any, Dict, List, Union, Optional, TYPE_CHECKING
from datamaxi.api import Resource
from datamaxi.resources.responses import PremiumResponse
from datamaxi.resources.utils import assemble_params, raise_if_no_data
from datamaxi.lib.constants import Market, SortOrder

if TYPE_CHECKING:
    import pandas as pd


def build_premium_params(
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
) -> Dict[str, Any]:
    """Assemble the ``premium`` endpoint's query params from caller args.

    Transport-agnostic (no request is made here) so the sync and async
    ``Premium.__call__`` methods share the exact same param-building logic —
    see #154.
    """
    return assemble_params(
        ("source_exchange", source_exchange),
        ("target_exchange", target_exchange),
        ("asset", asset),
        ("source_quote", source_quote),
        ("target_quote", target_quote),
        ("sort", sort),
        ("key", key),
        ("query", query),
        ("page", page),
        ("limit", limit),
        ("currency", currency),
        ("conversion_base", conversion_base),
        ("min_sv", min_sv),
        ("min_tv", min_tv),
        ("source_market", source_market),
        ("target_market", target_market),
        ("only_transferable", True if only_transferable else None),
        ("network", network),
        ("premium_type", premium_type),
        ("token_include", token_include),
        ("token_exclude", token_exclude),
    )


def shape_premium_response(
    res: PremiumResponse, pandas: bool
) -> Union[pd.DataFrame, PremiumResponse]:
    """Turn a raw ``premium`` response into the DataFrame or typed dict shape.

    Shared by the sync and async ``Premium.__call__`` so the "no data"
    check and DataFrame construction can't drift between the two — see
    #154.
    """
    raise_if_no_data(res)

    if not pandas:
        return res

    import pandas as pd

    return pd.DataFrame(
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

    def __call__(
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
        params = build_premium_params(
            source_exchange=source_exchange,
            target_exchange=target_exchange,
            asset=asset,
            source_quote=source_quote,
            target_quote=target_quote,
            sort=sort,
            key=key,
            page=page,
            limit=limit,
            currency=currency,
            conversion_base=conversion_base,
            min_sv=min_sv,
            min_tv=min_tv,
            source_market=source_market,
            target_market=target_market,
            only_transferable=only_transferable,
            network=network,
            premium_type=premium_type,
            token_include=token_include,
            token_exclude=token_exclude,
            query=query,
        )
        res = self.request_endpoint("premium", **params)
        return shape_premium_response(res, pandas)

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges for premium data.

        `GET /api/v1/premium/exchanges`

        <https://docs.datamaxiplus.com/rest/premium/exchanges>

        Returns:
            List of supported exchanges
        """
        return self.request_endpoint("premium_exchanges")
