"""Async client — ``httpx``-based mirror of the sync DataMaxi+ client.

Requires the ``async`` extra::

    pip install "datamaxi[async]"

Usage::

    from datamaxi.aio import AsyncDatamaxi

    async with AsyncDatamaxi(api_key="...") as client:
        df = await client.cex.candle(exchange="binance", market="spot",
                                     symbol="BTC-USDT")
        ticker = await client.cex.ticker.get(exchange="binance", market="spot",
                                             symbol="BTC-USDT")

Mirrors the full sync surface (``cex.*``, ``funding_rate``, ``forex``,
``premium``, ``liquidation``, ``open_interest``, ``margin_borrow``,
``index_price``, ``telegram``, ``naver``). Reuses the sync client's endpoint
resolution and error handling (``datamaxi._dispatch``) and the shared DataFrame
/ ResponseMeta helpers, so the two clients can't drift on request building or
error semantics.
"""

from datamaxi.aio._client import AsyncDatamaxi  # noqa: F401
from datamaxi.aio._core import AsyncAPI, AsyncResource  # noqa: F401
from datamaxi.aio.cex import (  # noqa: F401
    AsyncCex,
    AsyncCexCandle,
    AsyncCexTicker,
    AsyncCexFee,
    AsyncCexWalletStatus,
    AsyncCexAnnouncement,
    AsyncCexToken,
    AsyncCexSymbol,
)
from datamaxi.aio.funding_rate import AsyncFundingRate  # noqa: F401
from datamaxi.aio.forex import AsyncForex  # noqa: F401
from datamaxi.aio.premium import AsyncPremium  # noqa: F401
from datamaxi.aio.liquidation import AsyncLiquidation  # noqa: F401
from datamaxi.aio.open_interest import AsyncOpenInterest  # noqa: F401
from datamaxi.aio.margin_borrow import AsyncMarginBorrow  # noqa: F401
from datamaxi.aio.index_price import AsyncIndexPrice  # noqa: F401

__all__ = [
    "AsyncDatamaxi",
    "AsyncAPI",
    "AsyncResource",
    "AsyncCex",
    "AsyncCexCandle",
    "AsyncCexTicker",
    "AsyncCexFee",
    "AsyncCexWalletStatus",
    "AsyncCexAnnouncement",
    "AsyncCexToken",
    "AsyncCexSymbol",
    "AsyncFundingRate",
    "AsyncForex",
    "AsyncPremium",
    "AsyncLiquidation",
    "AsyncOpenInterest",
    "AsyncMarginBorrow",
    "AsyncIndexPrice",
]
