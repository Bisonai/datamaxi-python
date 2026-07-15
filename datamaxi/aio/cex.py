"""Async CEX resources — mirror of ``datamaxi.resources.cex`` + sub-resources."""

from __future__ import annotations

from typing import Any, List, Dict, Union, Optional, Tuple, Callable, TYPE_CHECKING

from datamaxi.aio._core import AsyncAPI, AsyncResource
from datamaxi.lib.utils import check_required_parameter, check_required_parameters
from datamaxi.resources.utils import raise_if_no_data, to_indexed_dataframe
from datamaxi.lib.constants import (
    SPOT,
    FUTURES,
    USD,
    INTERVAL_1D,
    ASC,
    DESC,
    Market,
    Interval,
    SortOrder,
)
from datamaxi.resources.responses import (
    CandleResponse,
    TickerResponse,
    WalletStatusRow,
    AnnouncementResponse,
    TokenUpdateResponse,
)

if TYPE_CHECKING:
    import pandas as pd


class AsyncCexCandle(AsyncResource):
    async def __call__(
        self,
        exchange: str,
        market: Market,
        symbol: str,
        currency: str = USD,
        interval: Interval = INTERVAL_1D,
        from_unix: Optional[str] = None,
        to_unix: Optional[str] = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, CandleResponse]:
        """Fetch candle data (async). See ``datamaxi.Datamaxi.cex.candle``."""
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [interval, "interval"],
                [market, "market"],
                [currency, "currency"],
            ]
        )
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        res = await self.request_endpoint(
            "cex_candle",
            exchange=exchange,
            market=market,
            symbol=symbol,
            interval=interval,
            currency=currency,
            **{"from": from_unix, "to": to_unix},
        )
        raise_if_no_data(res)

        if pandas:
            from datamaxi.resources.utils import convert_data_to_data_frame

            return convert_data_to_data_frame(res["data"])
        return res

    async def exchanges(self, market: Market) -> List[str]:
        check_required_parameter(market, "market")
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")
        return await self.request_endpoint("cex_candle_exchanges", market=market)

    async def symbols(
        self, exchange: Optional[str] = None, market: Optional[Market] = None
    ) -> List[Dict]:
        if market is not None and market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")
        return await self.request_endpoint(
            "cex_candle_symbols", exchange=exchange, market=market
        )

    async def intervals(self) -> List[str]:
        return await self.request_endpoint("cex_candle_intervals")


class AsyncCexTicker(AsyncResource):
    async def get(
        self,
        exchange: str,
        symbol: str,
        market: Market,
        currency: Optional[str] = None,
        conversion_base: Optional[str] = None,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, TickerResponse]:
        """Fetch ticker data (async). See ``datamaxi.Datamaxi.cex.ticker``."""
        check_required_parameters(
            [
                [exchange, "exchange"],
                [symbol, "symbol"],
                [market, "market"],
            ]
        )
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")

        res = await self.request_endpoint(
            "ticker",
            exchange=exchange,
            symbol=symbol,
            market=market,
            currency=currency,
            conversion_base=conversion_base,
        )

        if pandas:
            return to_indexed_dataframe([res["data"]], "d")
        return res

    async def exchanges(self, market: Market) -> List[str]:
        check_required_parameters([[market, "market"]])
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")
        return await self.request_endpoint("ticker_exchanges", market=market)

    async def symbols(self, exchange: str, market: Market) -> List[str]:
        check_required_parameters(
            [
                [exchange, "exchange"],
                [market, "market"],
            ]
        )
        if market not in [SPOT, FUTURES]:
            raise ValueError("market must be either spot or futures")
        return await self.request_endpoint(
            "ticker_symbols", exchange=exchange, market=market
        )


class AsyncCexFee(AsyncResource):
    async def __call__(
        self,
        exchange: Optional[str] = None,
        symbol: Optional[str] = None,
    ) -> List[Dict]:
        return await self.request_endpoint("cex_fees", exchange=exchange, symbol=symbol)

    async def exchanges(self) -> List[str]:
        return await self.request_endpoint("cex_fees_exchanges")

    async def symbols(self, exchange: str) -> List[str]:
        check_required_parameter(exchange, "exchange")
        return await self.request_endpoint("cex_fees_symbols", exchange=exchange)


class AsyncCexWalletStatus(AsyncResource):
    async def __call__(
        self,
        exchange: str,
        asset: str,
        pandas: bool = True,
    ) -> Union[pd.DataFrame, List[WalletStatusRow]]:
        check_required_parameters(
            [
                [exchange, "exchange"],
                [asset, "asset"],
            ]
        )
        res = await self.request_endpoint(
            "wallet_status", exchange=exchange, asset=asset
        )
        if pandas:
            return to_indexed_dataframe(res, "network")
        return res

    async def exchanges(self) -> List[str]:
        return await self.request_endpoint("wallet_status_exchanges")

    async def assets(self, exchange: str) -> List[str]:
        check_required_parameter(exchange, "exchange")
        return await self.request_endpoint("wallet_status_assets", exchange=exchange)


class AsyncCexAnnouncement(AsyncResource):
    async def __call__(
        self,
        page: int = 1,
        limit: int = 1000,
        sort: SortOrder = DESC,
        key: Optional[str] = None,
        exchange: Optional[str] = None,
        category: Optional[str] = None,
    ) -> Tuple[AnnouncementResponse, Callable]:
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if sort not in [ASC, DESC]:
            raise ValueError("sort must be either asc or desc")

        res = await self.request_endpoint(
            "cex_announcements",
            page=page,
            limit=limit,
            sort=sort,
            key=key,
            exchange=exchange,
            category=category,
        )
        if res["data"] is None:
            raise ValueError("no data found")

        async def next_request():
            return await self.__call__(
                key=key,
                exchange=exchange,
                category=category,
                page=page + 1,
                limit=limit,
                sort=sort,
            )

        return res, next_request


class AsyncCexToken(AsyncResource):
    async def updates(
        self,
        page: int = 1,
        limit: int = 1000,
        type: Optional[str] = None,
    ) -> Tuple[TokenUpdateResponse, Callable]:
        if page < 1:
            raise ValueError("page must be greater than 0")
        if limit < 1:
            raise ValueError("limit must be greater than 0")
        if type is not None and type not in ["listed", "delisted"]:
            raise ValueError("type must be either listed or delisted when set")

        res = await self.request_endpoint(
            "cex_token_updates", page=page, limit=limit, type=type
        )
        if res["data"] is None:
            raise ValueError("no data found")

        async def next_request():
            return await self.updates(
                type=type,
                page=page + 1,
                limit=limit,
            )

        return res, next_request


class AsyncCexSymbol(AsyncResource):
    async def metadata(
        self,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        market: Optional[str] = None,
        quote: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_metadata",
            exchange=exchange,
            base=base,
            market=market,
            quote=quote,
            status=status,
        )

    async def tags(
        self,
        exchange: Optional[str] = None,
        base: Optional[str] = None,
        tag: Optional[str] = None,
        market: Optional[str] = None,
        source: Optional[str] = None,
        min_confidence: Optional[int] = None,
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_tags",
            exchange=exchange,
            base=base,
            tag=tag,
            market=market,
            source=source,
            min_confidence=min_confidence,
        )

    async def cautions(
        self,
        exchange: Optional[str] = None,
        market: Optional[str] = None,
        min_level: Optional[str] = None,
        active_only: Optional[bool] = None,
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_cautions",
            exchange=exchange,
            market=market,
            min_level=min_level,
            active_only=active_only,
        )

    async def delistings(
        self,
        exchange: Optional[str] = None,
        market: Optional[str] = None,
        from_ms: Optional[int] = None,
        to_ms: Optional[int] = None,
        include_past: Optional[bool] = None,
    ) -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_delistings",
            exchange=exchange,
            market=market,
            from_ms=from_ms,
            to_ms=to_ms,
            include_past=include_past,
        )

    async def volume(self, base: str, market: Optional[str] = None) -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_volume", base=base, market=market
        )

    async def oi(self, base: str, exchange: Optional[str] = None) -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_oi", base=base, exchange=exchange
        )

    async def oi_stats(
        self,
        base: str,
        exchange: Optional[str] = None,
        currency: str = "USD",
    ) -> Dict[str, Any]:
        if currency not in ("USD", "KRW"):
            raise ValueError("currency must be either USD or KRW")
        return await self.request_endpoint(
            "cex_symbol_oi_stats",
            base=base,
            exchange=exchange,
            currency=currency,
        )

    async def liquidation(self, base: str, window: str = "24h") -> Dict[str, Any]:
        return await self.request_endpoint(
            "cex_symbol_liquidation", base=base, window=window
        )


class AsyncCex(AsyncResource):
    def __init__(self, api: "AsyncAPI"):
        super().__init__(api)
        self.candle = AsyncCexCandle(api)
        self.ticker = AsyncCexTicker(api)
        self.fee = AsyncCexFee(api)
        self.wallet_status = AsyncCexWalletStatus(api)
        self.announcement = AsyncCexAnnouncement(api)
        self.token = AsyncCexToken(api)
        self.symbol = AsyncCexSymbol(api)
