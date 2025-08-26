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
        min_pd: str = None,
        max_pd: str = None,
        min_pdp: str = None,
        max_pdp: str = None,
        min_pdp24h: str = None,
        max_pdp24h: str = None,
        min_pdp4h: str = None,
        max_pdp4h: str = None,
        min_pdp1h: str = None,
        max_pdp1h: str = None,
        min_pdp30m: str = None,
        max_pdp30m: str = None,
        min_pdp15m: str = None,
        max_pdp15m: str = None,
        min_pdp5m: str = None,
        max_pdp5m: str = None,
        min_dsp: str = None,
        max_dsp: str = None,
        min_dtp: str = None,
        max_dtp: str = None,
        min_spdp24h: str = None,
        max_spdp24h: str = None,
        min_spdp4h: str = None,
        max_spdp4h: str = None,
        min_spdp1h: str = None,
        max_spdp1h: str = None,
        min_spdp30m: str = None,
        max_spdp30m: str = None,
        min_spdp15m: str = None,
        max_spdp15m: str = None,
        min_spdp5m: str = None,
        max_spdp5m: str = None,
        min_sv: str = None,
        max_sv: str = None,
        min_tv: str = None,
        max_tv: str = None,
        min_net_funding_rate: str = None,
        max_net_funding_rate: str = None,
        min_source_funding_rate: str = None,
        max_source_funding_rate: str = None,
        min_target_funding_rate: str = None,
        max_target_funding_rate: str = None,
        source_market: str = None,
        target_market: str = None,
        only_transferable: bool = False,
        network: str = None,
        source_funding_rate_interval: str = None,
        target_funding_rate_interval: str = None,
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

            min_pd (str): Return results with price difference in USD above min_pd
            max_pd (str): Return results with price difference in USD below max_pd
            min_pdp (str): Return results with price difference percentage above min_pdp
            max_pdp (str): Return results with price difference percentage below max_pdp
            min_pdp24h (str): Return results with price difference percentage from 24h ago above min_pdp24h
            max_pdp24h (str): Return results with price difference percentage from 24h ago below max_pdp24h
            min_pdp4h (str): Return results with price difference percentage from 4h ago above min_pdp4h
            max_pdp4h (str): Return results with price difference percentage from 4h ago below max_pdp4h
            min_pdp1h (str): Return results with price difference percentage from 1h ago above min_pdp1h
            max_pdp1h (str): Return results with price difference percentage from 1h ago below max_pdp1h
            min_pdp30m (str): Return results with price difference percentage from 30m ago above min_pdp30m
            max_pdp30m (str): Return results with price difference percentage from 30m ago below max_pdp30m
            min_pdp15m (str): Return results with price difference percentage from 15m ago above min_pdp15m
            max_pdp15m (str): Return results with price difference percentage from 15m ago below max_pdp15m
            min_pdp5m (str): Return results with price difference percentage from 5m ago above min_pdp5m
            max_pdp5m (str): Return results with price difference percentage from 5m ago below max_pdp5m
            min_dsp (str): Return results with price in fiat on source exchange above min_dsp
            max_dsp (str): Return results with price in fiat on source exchange below max_dsp
            min_dtp (str): Return results with price in fiat on target exchange above min_dtp
            max_dtp (str): Return results with price in fiat on target exchange below max_dtp
            min_spdp24h (str): Return results with price difference percentage (between now and 24h ago on source exchange) above min_spdp24h
            max_spdp24h (str): Return results with price difference percentage (between now and 24h ago on source exchange) below max_spdp24h
            min_spdp4h (str): Return results with price difference percentage (between now and 4h ago on source exchange) above min_spdp4h
            max_spdp4h (str): Return results with price difference percentage (between now and 4h ago on source exchange) below max_spdp4h
            min_spdp1h (str): Return results with price difference percentage (between now and 1h ago on source exchange) above min_spdp1h
            max_spdp1h (str): Return results with price difference percentage (between now and 1h ago on source exchange) below max_spdp1h
            min_spdp30m (str): Return results with price difference percentage (between now and 30m ago on source exchange) above min_spdp30m
            max_spdp30m (str): Return results with price difference percentage (between now and 30m ago on source exchange) below max_spdp30m
            min_spdp15m (str): Return results with price difference percentage (between now and 15m ago on source exchange) above min_spdp15m
            max_spdp15m (str): Return results with price difference percentage (between now and 15m ago on source exchange) below max_spdp15m
            min_spdp5m (str): Return results with price difference percentage (between now and 5m ago on source exchange) above min_spdp5m
            max_spdp5m (str): Return results with price difference percentage (between now and 5m ago on source exchange) below max_spdp5m
            min_sv (str): Return results with 24h volume in fiat on source exchange above min_sv
            max_sv (str): Return results with 24h volume in fiat on source exchange below max_sv
            min_tv (str): Return results with 24h volume in fiat on target exchange above min_tv
            max_tv (str): Return results with 24h volume in fiat on target exchange below max_tv
            min_net_funding_rate (str): Return results with net funding rate above min_net_funding_rate
            max_net_funding_rate (str): Return results with net funding rate below max_net_funding_rate
            min_source_funding_rate (str): Return results with source funding rate above min_source_funding_rate
            max_source_funding_rate (str): Return results with source funding rate below max_source_funding_rate
            min_target_funding_rate (str): Return results with target funding rate above min_target_funding_rate
            max_target_funding_rate (str): Return results with target funding rate below max_target_funding_rate
            source_market (str): Return results matching source market
            target_market (str): Return results matching target market
            only_transferable (bool): Return only transferable if set true
            network (str): Return results containing only specified network
            source_funding_rate_interval (str): Return results with min source funding rate interval
            target_funding_rate_interval (str): Return results with min target funding rate interval
            premium_type (str): Return based on matching premium_type
            token_include (str): Return results containing only specified token
            token_exclude (str): Return results not containing specified token

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

        if min_pd is not None:
            params["min_pd"] = min_pd

        if max_pd is not None:
            params["max_pd"] = max_pd

        if min_pdp is not None:
            params["min_pdp"] = min_pdp

        if max_pdp is not None:
            params["max_pdp"] = max_pdp

        if min_pdp24h is not None:
            params["min_pdp24h"] = min_pdp24h

        if max_pdp24h is not None:
            params["max_pdp24h"] = max_pdp24h

        if min_pdp4h is not None:
            params["min_pdp4h"] = min_pdp4h

        if max_pdp4h is not None:
            params["max_pdp4h"] = max_pdp4h

        if min_pdp1h is not None:
            params["min_pdp1h"] = min_pdp1h

        if max_pdp1h is not None:
            params["max_pdp1h"] = max_pdp1h

        if min_pdp30m is not None:
            params["min_pdp30m"] = min_pdp30m

        if max_pdp30m is not None:
            params["max_pdp30m"] = max_pdp30m

        if min_pdp15m is not None:
            params["min_pdp15m"] = min_pdp15m

        if max_pdp15m is not None:
            params["max_pdp15m"] = max_pdp15m

        if min_pdp5m is not None:
            params["min_pdp5m"] = min_pdp5m

        if max_pdp5m is not None:
            params["max_pdp5m"] = max_pdp5m

        if min_dsp is not None:
            params["min_dsp"] = min_dsp

        if max_dsp is not None:
            params["max_dsp"] = max_dsp

        if min_dtp is not None:
            params["min_dtp"] = min_dtp

        if max_dtp is not None:
            params["max_dtp"] = max_dtp

        if min_spdp24h is not None:
            params["min_spdp24h"] = min_spdp24h

        if max_spdp24h is not None:
            params["max_spdp24h"] = max_spdp24h

        if min_spdp4h is not None:
            params["min_spdp4h"] = min_spdp4h

        if max_spdp4h is not None:
            params["max_spdp4h"] = max_spdp4h

        if min_spdp1h is not None:
            params["min_spdp1h"] = min_spdp1h

        if max_spdp1h is not None:
            params["max_spdp1h"] = max_spdp1h

        if min_spdp30m is not None:
            params["min_spdp30m"] = min_spdp30m

        if max_spdp30m is not None:
            params["max_spdp30m"] = max_spdp30m

        if min_spdp15m is not None:
            params["min_spdp15m"] = min_spdp15m

        if max_spdp15m is not None:
            params["max_spdp15m"] = max_spdp15m

        if min_spdp5m is not None:
            params["min_spdp5m"] = min_spdp5m

        if max_spdp5m is not None:
            params["max_spdp5m"] = max_spdp5m

        if min_sv is not None:
            params["min_sv"] = min_sv

        if max_sv is not None:
            params["max_sv"] = max_sv

        if min_tv is not None:
            params["min_tv"] = min_tv

        if max_tv is not None:
            params["max_tv"] = max_tv

        if min_net_funding_rate is not None:
            params["min_net_funding_rate"] = min_net_funding_rate

        if max_net_funding_rate is not None:
            params["max_net_funding_rate"] = max_net_funding_rate

        if min_source_funding_rate is not None:
            params["min_source_funding_rate"] = min_source_funding_rate

        if max_source_funding_rate is not None:
            params["max_source_funding_rate"] = max_source_funding_rate

        if min_target_funding_rate is not None:
            params["min_target_funding_rate"] = min_target_funding_rate

        if max_target_funding_rate is not None:
            params["max_target_funding_rate"] = max_target_funding_rate

        if source_market is not None:
            params["source_market"] = source_market

        if target_market is not None:
            params["target_market"] = target_market

        if only_transferable:
            params["only_transferable"] = True

        if network is not None:
            params["network"] = network

        if source_funding_rate_interval is not None:
            params["source_funding_rate_interval"] = source_funding_rate_interval

        if target_funding_rate_interval is not None:
            params["target_funding_rate_interval"] = target_funding_rate_interval

        if premium_type is not None:
            params["premium_type"] = premium_type

        if token_include is not None:
            params["token_include"] = token_include

        if token_exclude is not None:
            params["token_exclude"] = token_exclude

        res = self.query("/api/v1/premium", params)
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
        """Fetch supported exchanges accepted by
        [datamaxi.Premium.get](#datamaxi.datamaxi.Premium.get)
        API.

        `GET /api/v1/Premium/exchanges`

        <https://docs.datamaxiplus.com/rest/Premium/exchanges>

        Returns:
            List of supported exchange
        """
        url_path = "/api/v1/premium/exchanges"
        return self.query(url_path)
