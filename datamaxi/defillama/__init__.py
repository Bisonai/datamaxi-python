from typing import Any, List, Union
import pandas as pd
from datamaxi.api import API
from datamaxi.lib.utils import check_required_parameter
from datamaxi.lib.utils import check_required_parameters
from datamaxi.lib.utils import check_required_parameter_list
from datamaxi.lib.utils import encode_string_list
from datamaxi.lib.utils import make_list
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

        <https://docs.neverest.finance/defillama/protocol>

        Returns:
            List of supported protocols
        """
        url_path = "/v1/defillama/protocol"
        return self.query(url_path)

    def chains(self) -> List[str]:
        """Get supported chains

        `GET /v1/defillama/chain`

        <https://docs.neverest.finance/defillama/chain>

        Returns:
            List of supported chains
        """
        url_path = "/v1/defillama/chain"
        return self.query(url_path)

    def tokens(self) -> List[str]:
        """Get supported tokens

        `GET /v1/defillama/token`

        <https://docs.neverest.finance/defillama/token>

        Returns:
            List of supported tokens
        """
        url_path = "/v1/defillama/token"
        return self.query(url_path)

    def pools(self) -> List[str]:
        """Get supported pools

        `GET /v1/defillama/pool`

        <https://docs.neverest.finance/defillama/pool>

        Returns:
            List of supported pools
        """
        url_path = "/v1/defillama/pool"
        return self.query(url_path)

    def stablecoins(self) -> List[str]:
        """Get supported stablecoins

        `GET /v1/defillama/stablecoin`

        <https://docs.neverest.finance/defillama/stablecoin>

        Returns:
            List of supported stablecoins
        """
        url_path = "/v1/defillama/stablecoin"
        return self.query(url_path)

    @postprocess()
    def tvl(self, pandas: bool = True) -> Union[List, pd.DataFrame]:
        """Get total TVL across all chains and protocols

        `GET /v1/defillama/tvl`

        <https://docs.neverest.finance/defillama/tvl>

        Args:
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of total TVL
        """
        url_path = "/v1/defillama/tvl"
        return self.query(url_path)

    @postprocess()
    def protocol_tvl(
        self, protocols: Union[str, List[str]] = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get TVL for given protocols

        `GET /v1/defillama/tvl`

        <https://docs.neverest.finance/defillama/tvl>

        Args:
            protocols (Union[str, List[str]]): single protocol or multiple protocol names
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of protocol TVLs
        """
        protocols = make_list(protocols)
        check_required_parameter_list(protocols, "protocols")
        params = {"protocols": encode_string_list(protocols)}
        return self.query("/v1/defillama/tvl", params)

    @postprocess()
    def chain_tvl(
        self, chains: Union[str, List[str]] = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get TVL for given chains

        `GET /v1/defillama/tvl`

        <https://docs.neverest.finance/defillama/tvl>

        Args:
            chains (Union[str, List[str]]): single chain or multiple chain names
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of chain TVLs
        """
        chains = make_list(chains)
        check_required_parameter_list(chains, "chains")
        params = {"chains": encode_string_list(chains)}
        return self.query("/v1/defillama/tvl", params)

    @postprocess()
    def protocol_chain_tvl(
        self, protocol: str, chain: str, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get TVL for given protocol and chain

        `GET /v1/defillama/tvl`

        <https://docs.neverest.finance/defillama/tvl>

        Args:
            protocol (str): protocol name
            chain (str): chain name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of protocol TVL on a given chain
        """
        check_required_parameters([[protocol, "protocol"], [chain, "chain"]])
        params = {"chain": chain, "protocol": protocol}
        return self.query("/v1/defillama/tvl", params)

    @postprocess(num_index=2)
    def protocol_token_tvl(
        self, protocol: str, usd: bool = True, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get token TVL on a given protocol

        `GET /v1/defillama/tvl`

        <https://docs.neverest.finance/defillama/tvl>

        Args:
            protocol (str): protocol name
            usd (bool): Convert to USD otherwise return token amount
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of token TVL for a given protocol
        """
        check_required_parameters([[protocol, "protocol"], [usd, "usd"]])
        params = {
            "protocol": protocol,
            "token": "true",
            "usd": str(usd).lower(),
        }
        return self.query("/v1/defillama/tvl", params)

    @postprocess(num_index=2)
    def protocol_chain_token_tvl(
        self, protocol: str, chain: str, usd: bool = True, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get token TVL on a given protocol and chain

        `GET /v1/defillama/tvl`

        <https://docs.neverest.finance/defillama/tvl>

        Args:
            protocol (str): protocol name
            chain (str): chain name
            usd (bool): Convert to USD otherwise return token amount
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of token TVL for a given protocol and chain
        """
        check_required_parameters(
            [[protocol, "protocol"], [chain, "chain"], [usd, "usd"]]
        )
        params = {
            "protocol": protocol,
            "chain": chain,
            "token": "true",
            "usd": str(usd).lower(),
        }
        return self.query("/v1/defillama/tvl", params)

    @postprocess()
    def protocol_mcap(
        self, protocols: Union[str, List[str]] = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get market cap for given protocols

        `GET /v1/defillama/mcap`

        <https://docs.neverest.finance/defillama/mcap>

        Args:
            protocols (Union[str, List[str]]): single protocol or multiple protocol names
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of market cap for given protocols
        """
        protocols = make_list(protocols)
        check_required_parameter_list(protocols, "protocols")
        params = {
            "protocols": encode_string_list(protocols),
        }
        return self.query("/v1/defillama/mcap", params)

    @postprocess()
    def token_price(
        self, addresses: Union[str, List[str]] = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get token prices

        `GET /v1/defillama/token`

        <https://docs.neverest.finance/defillama/token-price>

        Args:
            addresses (Union[str, List[str]]): single address or multiple addresses
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of token prices
        """
        addresses = make_list(addresses)
        check_required_parameter_list(addresses, "addresses")
        params = {
            "addresses": encode_string_list(addresses),
        }
        return self.query("/v1/defillama/token", params)

    # def yields(self, pools: Union[str, List[str]]=None) -> pd.DataFrame:
    #     pools = make_list(pools)
    #     check_required_parameter_list(pools, "pools")
    #     params = {
    #         "poolIds": encode_string_list(pools),
    #     }
    #     return self.query("/v1/defillama/yield", params)

    @postprocess()
    def stablecoin_mcap(
        self, stablecoin: str = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get market cap for given stablecoin

        `GET /v1/defillama/stablecoin`

        <https://docs.neverest.finance/defillama/stablecoin-mcap>

        Args:
            stablecoin (str): stablecoin name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of market cap for given stablecoin
        """
        check_required_parameter_list(stablecoin, "stablecoin")
        params = {
            "stablecoin": stablecoin,
        }
        return self.query("/v1/defillama/stablecoin", params)

    @postprocess()
    def stablecoin_chain_mcap(
        self, stablecoin: str, chain: str, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get market cap for a given stablecoin on a specific chain

        `GET /v1/defillama/stablecoin`

        <https://docs.neverest.finance/defillama/stablecoin-mcap>

        Args:
            stablecoin (str): stablecoin name
            chain (str): chain name
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of market cap for given stablecoin on a specific chain
        """
        check_required_parameters([[stablecoin, "stablecoin"], [chain, "chain"]])
        params = {
            "stablecoin": stablecoin,
            "chain": chain,
        }
        return self.query("/v1/defillama/stablecoin", params)

    @postprocess()
    def stablecoin_price(
        self, stablecoins: Union[str, List[str]] = None, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get price for given stablecoins

        `GET /v1/defillama/stablecoin/price`

        <https://docs.neverest.finance/defillama/stablecoin-price>

        Args:
            stablecoins (Union[str, List[str]]): single stablecoin or multiple stablecoin names
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of stablecoin prices
        """
        stablecoins = make_list(stablecoins)
        check_required_parameter_list(stablecoins, "stablecoins")
        params = {
            "stablecoins": encode_string_list(stablecoins),
        }
        return self.query("/v1/defillama/stablecoin/price", params)

    @postprocess()
    def fee(
        self,
        protocols: Union[str, List[str]] = None,
        chains: Union[str, List[str]] = None,
        daily: bool = True,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get fee for given protocols or chains

        `GET /v1/defillama/fee`

        <https://docs.neverest.finance/defillama/fee>

        Args:
            protocols (Union[str, List[str]]): single protocol or multiple protocol names
            chains (Union[str, List[str]]): single chain or multiple chain names
            daily (bool): daily fee or total fee
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of protocol or fees
        """
        check_required_parameter(daily, "daily")
        params = {
            "daily": str(daily).lower(),
        }

        if not ((protocols is None) ^ (chains is None)):
            raise ValueError("Either protocols or chains should be provided")

        if protocols is not None:
            protocols = make_list(protocols)
            check_required_parameter_list(protocols, "protocols")
            params["protocols"] = encode_string_list(protocols)
        elif chains is not None:
            chains = make_list(chains)
            check_required_parameter_list(chains, "chains")
            params["chains"] = encode_string_list(chains)

        return self.query("/v1/defillama/fee", params)

    @postprocess()
    def revenue(
        self,
        protocols: Union[str, List[str]] = None,
        chains: Union[str, List[str]] = None,
        daily: bool = True,
        pandas: bool = True,
    ) -> Union[List, pd.DataFrame]:
        """Get revenue for given protocols or chains

        `GET /v1/defillama/revenue`

        <https://docs.neverest.finance/defillama/revenue>

        Args:
            protocols (Union[str, List[str]]): single protocol or multiple protocol names
            chains (Union[str, List[str]]): single chain or multiple chain names
            daily (bool): daily revenue or total revenue
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of protocol or chain revenues
        """
        check_required_parameter(daily, "daily")
        params = {
            "daily": str(daily).lower(),
        }

        if not ((protocols is None) ^ (chains is None)):
            raise ValueError("Either protocols or chains should be provided")

        if protocols is not None:
            protocols = make_list(protocols)
            check_required_parameter_list(protocols, "protocols")
            params["protocols"] = encode_string_list(protocols)
        elif chains is not None:
            chains = make_list(chains)
            check_required_parameter_list(chains, "chains")
            params["chains"] = encode_string_list(chains)

        return self.query("/v1/defillama/revenue", params)

    @postprocess(num_index=4)
    def fee_detail(
        self, protocol: str, chain: str = None, daily: bool = True, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get fee detail for given protocol and chain

        `GET /v1/defillama/fee/detail`

        <https://docs.neverest.finance/defillama/fee-detail>

        Args:
            protocol (str): protocol name
            chain (str): chain name (optional)
            daily (bool): daily fee or total fee
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of fee detail for a given protocol and chain
        """
        check_required_parameters([[protocol, "protocol"], [daily, "daily"]])
        params = {
            "protocol": protocol,
            "daily": str(daily).lower(),
        }
        if chain is not None:
            params["chain"] = chain

        return self.query("/v1/defillama/fee/detail", params)

    @postprocess(num_index=4)
    def revenue_detail(
        self, protocol: str, chain: str = None, daily: bool = True, pandas: bool = True
    ) -> Union[List, pd.DataFrame]:
        """Get revenue detail for given protocol and chain

        `GET /v1/defillama/revenue/detail`

        <https://docs.neverest.finance/defillama/revenue-detail>

        Args:
            protocol (str): protocol name
            chain (str): chain name (optional)
            daily (bool): daily revenue or total revenue
            pandas (bool): Return data as pandas DataFrame

        Returns:
            Timeseries of revenue detail for a given protocol and chain
        """
        check_required_parameters([[protocol, "protocol"], [daily, "daily"]])
        params = {
            "protocol": protocol,
            "daily": str(daily).lower(),
        }
        if chain is not None:
            params["chain"] = chain

        return self.query("/v1/defillama/revenue/detail", params)
