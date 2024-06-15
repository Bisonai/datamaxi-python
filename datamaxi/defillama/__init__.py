from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_at_least_one_set_parameters
from datamaxi.lib.utils import postprocess
from datamaxi.lib.constants import BASE_URL


class Defillama(API):
    """Client to fetch Defillama data from DataMaxi+ API."""

    def __init__(self, api_key=None, **kwargs: Any):
        """Initialize the object.

        Args:
            api_key (str): The DataMaxi+ API key
            **kwargs: Keyword arguments used by `datamaxi.api.API`.
        """
        if "base_url" not in kwargs:
            kwargs["base_url"] = BASE_URL
        super().__init__(api_key, **kwargs)

    def protocols(self) -> List[str]:
        """Get supported protocols

        `GET /v1/defillama/protocol`

        <https://docs.datamaxiplus.com/api/datasets/defillama/protocol>

        Returns:
            List of supported protocols
        """
        url_path = "/v1/defillama/protocol"
        return self.query(url_path)

    def chains(self) -> List[str]:
        """Get supported chains

        `GET /v1/defillama/chain`

        <https://docs.datamaxiplus.com/api/datasets/defillama/chain>

        Returns:
            List of supported chains
        """
        url_path = "/v1/defillama/chain"
        return self.query(url_path)

    def pools(self) -> List[str]:
        """Get supported pools

        `GET /v1/defillama/pool`

        <https://docs.datamaxiplus.com/api/datasets/defillama/pool>

        Returns:
            List of supported pools
        """
        url_path = "/v1/defillama/pool"
        return self.query(url_path)

    def stablecoins(self) -> List[str]:
        """Get supported stablecoins

        `GET /v1/defillama/stablecoin`

        <https://docs.datamaxiplus.com/api/datasets/defillama/stablecoin>

        Returns:
            List of supported stablecoins
        """
        url_path = "/v1/defillama/stablecoin"
        return self.query(url_path)

    @postprocess()
    def tvl(
        self, protocol: str = None, chain: str = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get total TVL across all chains and protocols

        `GET /v1/defillama/tvl`

        <https://docs.datamaxiplus.com/api/datasets/defillama/tvl>

        Args:
            protocol (str): Protocol name
            chain (str): Chain name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of total TVL
        """
        params = {}
        if protocol is not None:
            params["protocol"] = protocol

        if chain is not None:
            params["chain"] = chain

        url_path = "/v1/defillama/tvl"
        return self.query(url_path, params)

    @postprocess(num_index=2)
    def tvl_detail(
        self, protocol: str, chain: str = None, token: bool = False, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get TVL detail for given protocol and chain

        `GET /v1/defillama/tvl/detail`

        <https://docs.datamaxiplus.com/api/datasets/defillama/tvl-detail>

        Args:
            protocol (str): Protocol name
            chain (str): Chain name
            token (bool): Return token amount (return by default USD)
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of TVL detail for a given protocol and chain
        """
        check_required_parameter(protocol, "protocol")
        params = {"protocol": protocol}

        if chain is not None:
            params["chain"] = chain

        if token:
            params["token"] = str(token).lower()

        url_path = "/v1/defillama/tvl/detail"
        return self.query(url_path, params)

    @postprocess()
    def mcap(self, protocol: str, pandas: bool = True) -> Union[List, pd.DataFrame]:
        """Get market cap for given protocol

        `GET /v1/defillama/mcap`

        <https://docs.datamaxiplus.com/api/datasets/defillama/mcap>

        Args:
            protocol (str): Protocol name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of market cap for given protocol
        """
        check_required_parameter(protocol, "protocol")
        params = {
            "protocol": protocol,
        }
        return self.query("/v1/defillama/mcap", params)

    @postprocess()
    def pool_yield(self, poolId: str, pandas: bool = True) -> Union[List, pd.DataFrame]:
        """Get yield for given pool

        `GET /v1/defillama/pool/yield`

        <https://docs.datamaxiplus.com/api/datasets/defillama/pool-yield>

        Args:
            poolId (str): Pool ID
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of yield for given pool
        """
        check_required_parameter(poolId, "poolId")
        params = {
            "poolId": poolId,
        }
        return self.query("/v1/defillama/pool/yield", params)

    @postprocess()
    def stablecoin_mcap(
        self, stablecoin: str, chain: str = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get market cap for given stablecoin and chain

        `GET /v1/defillama/stablecoin/mcap`

        <https://docs.datamaxiplus.com/api/datasets/defillama/stablecoin-mcap>

        Args:
            stablecoin (str): Stablecoin name
            chain (str): Chain name (optional)
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of market cap for given stablecoin and chain
        """
        check_required_parameter(stablecoin, "stablecoin")
        params = {
            "stablecoin": stablecoin,
        }

        if chain is not None:
            params["chain"] = chain

        return self.query("/v1/defillama/stablecoin/mcap", params)

    @postprocess()
    def stablecoin_price(
        self, stablecoin: str, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get price for given stablecoin

        `GET /v1/defillama/stablecoin/price`

        <https://docs.datamaxiplus.com/api/datasets/defillama/stablecoin-price>

        Args:
            stablecoin (str): Stablecoin name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of stablecoin prices
        """
        check_required_parameter(stablecoin, "stablecoin")
        params = {
            "stablecoin": stablecoin,
        }
        return self.query("/v1/defillama/stablecoin/price", params)

    @postprocess()
    def fee(
        self,
        protocol: str = None,
        chain: str = None,
        daily: bool = True,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get fee for given protocol or chain

        `GET /v1/defillama/fee`

        <https://docs.datamaxiplus.com/api/datasets/defillama/fee>

        Args:
            protocol (str): Protocol name
            chain (str): Chain name
            daily (bool): Daily fee or total fee
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of protocol or fees
        """
        check_required_parameter(daily, "daily")
        params = {
            "daily": str(daily).lower(),
        }

        if not ((protocol is None) ^ (chain is None)):
            raise ValueError("Either protocols or chains should be provided")

        if protocol is not None:
            check_required_parameter(protocol, "protocol")
            params["protocol"] = protocol
        elif chain is not None:
            check_required_parameter(chain, "chain")
            params["chain"] = chain

        return self.query("/v1/defillama/fee", params)

    @postprocess()
    def revenue(
        self,
        protocol: str = None,
        chain: str = None,
        daily: bool = True,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get revenue for given protocol or chain

        `GET /v1/defillama/revenue`

        <https://docs.datamaxiplus.com/api/datasets/defillama/revenue>

        Args:
            protocol (str): Protocol name
            chain (str): Chain name
            daily (bool): Daily revenue or total revenue
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of protocol or chain revenues
        """
        check_required_parameter(daily, "daily")
        params = {
            "daily": str(daily).lower(),
        }

        if not ((protocol is None) ^ (chain is None)):
            raise ValueError("Either protocols or chains should be provided")

        if protocol is not None:
            check_required_parameter(protocol, "protocol")
            params["protocol"] = protocol
        elif chain is not None:
            check_required_parameter(chain, "chain")
            params["chain"] = chain

        return self.query("/v1/defillama/revenue", params)

    @postprocess(num_index=-1)
    def fee_detail(
        self,
        protocol: str = None,
        chain: str = None,
        daily: bool = True,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get fee detail for given protocol and chain

        `GET /v1/defillama/fee/detail`

        <https://docs.datamaxiplus.com/api/datasets/defillama/fee-detail>

        Args:
            protocol (str): Protocol name
            chain (str): Chain name
            daily (bool): Daily fee or total fee
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of fee detail for a given protocol and chain
        """
        check_required_parameter(daily, "daily")
        params = {
            "daily": str(daily).lower(),
        }

        check_at_least_one_set_parameters([[protocol, "protocol"], [chain, "chain"]])
        if protocol is not None:
            params["protocol"] = protocol

        if chain is not None:
            params["chain"] = chain

        return self.query("/v1/defillama/fee/detail", params)

    @postprocess(num_index=-1)
    def revenue_detail(
        self,
        protocol: str = None,
        chain: str = None,
        daily: bool = True,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get revenue detail for given protocol and chain

        `GET /v1/defillama/revenue/detail`

        <https://docs.datamaxiplus.com/api/datasets/defillama/revenue-detail>

        Args:
            protocol (str): Protocol name
            chain (str): Chain name
            daily (bool): Daily revenue or total revenue
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of revenue detail for a given protocol and chain
        """
        check_required_parameter(daily, "daily")
        params = {
            "daily": str(daily).lower(),
        }

        check_at_least_one_set_parameters([[protocol, "protocol"], [chain, "chain"]])
        if protocol is not None:
            params["protocol"] = protocol

        if chain is not None:
            params["chain"] = chain

        return self.query("/v1/defillama/revenue/detail", params)
