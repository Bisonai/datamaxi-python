from typing import Any, Callable, Tuple, List, Dict, Union
import logging
from datamaxi.api import API
import pandas as pd
from datamaxi.lib.utils import check_required_parameters
from datamaxi.datamaxi.utils import convert_data_to_data_frame
from datamaxi.lib.constants import ASC, DESC


class Dex(API):
    """Client to fetch DEX data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize DEX client.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        super().__init__(api_key, **kwargs)

    def trade(
        self,
        chain: str,
        exchange: str,
        pool: str,
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: str = "desc",
        pandas: bool = True,
    ) -> Union[Tuple[Dict, Callable], Tuple[pd.DataFrame, Callable]]:
        """Fetch DEX trade data

        `GET /api/v1/dex/trade`

        <https://docs.datamaxiplus.com/rest/dex/trade>

        Args:
            chain (str): Chain name
            exchange (str): Exchange name
            pool (str): Pool name
            page (int): Page number
            limit (int): Limit of data
            fromDateTime (str): Start date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            toDateTime (str): End date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            sort (str): Sort order
            pandas (bool): Return data as pandas DataFrame

        Returns:
            DEX trade data in pandas DataFrame and next request function
        """
        logging.warning("warning: dex related endpoints are experimental")

        check_required_parameters(
            [
                [chain, "chain"],
                [exchange, "exchange"],
                [pool, "pool"],
            ]
        )
        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if fromDateTime is not None and toDateTime is not None:
            raise ValueError(
                "fromDateTime and toDateTime cannot be set at the same time"
            )

        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "chain": chain,
            "exchange": exchange,
            "pool": pool,
            "page": page,
            "limit": limit,
            "from": fromDateTime,
            "to": toDateTime,
            "sort": sort,
        }

        res = self.query("/api/v1/dex/trade", params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                chain,
                exchange,
                pool,
                page + 1,
                limit,
                fromDateTime,
                toDateTime,
                sort,
                pandas,
            )

        if pandas:
            df = convert_data_to_data_frame(res["data"], ["b", "bq", "qq", "p"])
            return df, next_request
        else:
            return res, next_request

    def candle(
        self,
        chain: str,
        exchange: str,
        pool: str,
        interval: str = "1d",
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: str = "desc",
        pandas: bool = True,
    ) -> Union[Tuple[Dict, Callable], Tuple[pd.DataFrame, Callable]]:
        """Fetch DEX candle data

        `GET /api/v1/dex/candle`

        <https://docs.datamaxiplus.com/rest/dex/candle>

        Args:
            chain (str): Chain name
            exchange (str): Exchange name
            pool (str): Pool name
            interval (str): Candle interval
            page (int): Page number
            limit (int): Limit of data
            fromDateTime (str): Start date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            toDateTime (str): End date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            sort (str): Sort order
            pandas (bool): Return data as pandas DataFrame

        Returns:
            DEX candle data in pandas DataFrame and next request function
        """
        logging.warning("warning: dex related endpoints are experimental")

        check_required_parameters(
            [
                [chain, "chain"],
                [exchange, "exchange"],
                [pool, "pool"],
                [interval, "interval"],
            ]
        )

        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if fromDateTime is not None and toDateTime is not None:
            raise ValueError(
                "fromDateTime and toDateTime cannot be set at the same time"
            )

        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "chain": chain,
            "exchange": exchange,
            "pool": pool,
            "interval": interval,
            "page": page,
            "limit": limit,
            "from": fromDateTime,
            "to": toDateTime,
            "sort": sort,
        }

        res = self.query("/api/v1/dex/candle", params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                chain,
                exchange,
                pool,
                interval,
                page + 1,
                limit,
                fromDateTime,
                toDateTime,
                sort,
                pandas,
            )

        if pandas:
            df = convert_data_to_data_frame(res["data"])
            return df, next_request
        else:
            return res, next_request

    def liquidity(
        self,
        chain: str,
        exchange: str,
        pool: str,
        page: int = 1,
        limit: int = 1000,
        fromDateTime: str = None,
        toDateTime: str = None,
        sort: str = "desc",
        pandas: bool = True,
    ) -> Union[Tuple[Dict, Callable], Tuple[pd.DataFrame, Callable]]:
        """Fetch DEX liquidity data

        `GET /api/v1/dex/liquidity`

        <https://docs.datamaxiplus.com/rest/dex/liquidity>

        Args:
            chain (str): Chain name
            exchange (str): Exchange name
            pool (str): Pool name
            page (int): Page number
            limit (int): Limit of data
            fromDateTime (str): Start date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            toDateTime (str): End date and time (accepts format "2006-01-02 15:04:05" or "2006-01-02")
            sort (str): Sort order
            pandas (bool): Return data as pandas DataFrame

        Returns:
            DEX liquidity data in pandas DataFrame and next request function
        """
        logging.warning("warning: dex related endpoints are experimental")

        check_required_parameters(
            [
                [chain, "chain"],
                [exchange, "exchange"],
                [pool, "pool"],
            ]
        )

        if page < 1:
            raise ValueError("page must be greater than 0")

        if limit < 1:
            raise ValueError("limit must be greater than 0")

        if fromDateTime is not None and toDateTime is not None:
            raise ValueError(
                "fromDateTime and toDateTime cannot be set at the same time"
            )

        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        params = {
            "chain": chain,
            "exchange": exchange,
            "pool": pool,
            "page": page,
            "limit": limit,
            "from": fromDateTime,
            "to": toDateTime,
            "sort": sort,
        }

        res = self.query("/api/v1/dex/liquidity", params)
        if res["data"] is None or len(res["data"]) == 0:
            raise ValueError("no data found")

        def next_request():
            return self.get(
                chain,
                exchange,
                pool,
                page + 1,
                limit,
                fromDateTime,
                toDateTime,
                sort,
                pandas,
            )

        if pandas:
            df = convert_data_to_data_frame(
                res["data"],
            )
            return df, next_request
        else:
            return res, next_request

    def chains(self) -> List[str]:
        """Fetch supported chains accepted by
        [datamaxi.Dex.candle](./#datamaxi.datamaxi.Dex.candle),
        [datamaxi.Dex.trade](./#datamaxi.datamaxi.Dex.trade) and
        [datamaxi.Dex.liquidity](./#datamaxi.datamaxi.Dex.liquidity).

        `GET /api/v1/dex/chains`

        <https://docs.datamaxiplus.com/rest/dex/chains>

        Returns:
            List of supported chains
        """
        logging.warning("warning: dex related endpoints are experimental")

        url_path = "/api/v1/dex/chains"
        return self.query(url_path)

    def exchanges(self) -> List[str]:
        """Fetch supported exchanges accepted by
        [datamaxi.Dex.candle](./#datamaxi.datamaxi.Dex.candle),
        [datamaxi.Dex.trade](./#datamaxi.datamaxi.Dex.trade) and
        [datamaxi.Dex.liquidity](./#datamaxi.datamaxi.Dex.liquidity).

        `GET /api/v1/dex/exchanges`

        <https://docs.datamaxiplus.com/rest/dex/exchanges>

        Returns:
            List of supported exchanges
        """
        logging.warning("warning: dex related endpoints are experimental")

        url_path = "/api/v1/dex/exchanges"
        return self.query(url_path)

    def pools(self, exchange: str = None, chain: str = None) -> List[Dict]:
        """Fetch supported pools accepted by
        [datamaxi.Dex.candle](./#datamaxi.datamaxi.Dex.candle),
        [datamaxi.Dex.trade](./#datamaxi.datamaxi.Dex.trade) and
        [datamaxi.Dex.liquidity](./#datamaxi.datamaxi.Dex.liquidity).

        `GET /api/v1/dex/pools`

        <https://docs.datamaxiplus.com/rest/dex/pools>

        Args:
            exchange (str): Exchange name
            chain (str): Chain name (applied to DEX only)

        Returns:
            List of supported pools
        """
        params = {}
        if exchange is not None:
            params["exchange"] = exchange
        if chain is not None:
            params["chain"] = chain

        url_path = "/api/v1/dex/pools"
        return self.query(url_path, params)

    def intervals(self) -> List[str]:
        """Fetch supported intervals accepted by
        [datamaxi.Dex.candle](./#datamaxi.datamaxi.Dex.candle).

        `GET /api/v1/dex/intervals`

        <https://docs.datamaxiplus.com/rest/dex/intervals>

        Returns:
            List of supported intervals
        """
        logging.warning("warning: dex related endpoints are experimental")

        url_path = "/api/v1/dex/intervals"
        return self.query(url_path)
