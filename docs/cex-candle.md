# CEX Candle

Historical OHLCV candle data for centralized exchanges.

## Usage

=== "Sync"

    ```python
    from datamaxi import Datamaxi

    maxi = Datamaxi(api_key="YOUR_API_KEY")

    exchanges = maxi.cex.candle.exchanges(market="spot")
    symbols = maxi.cex.candle.symbols(exchange="binance", market="spot")
    intervals = maxi.cex.candle.intervals()

    df = maxi.cex.candle(
        exchange="binance",
        symbol="BTC-USDT",
        interval="1d",
        market="spot",
        from_unix=1704067200,
        to_unix=1706745600,
    )
    ```

=== "Async"

    ```python
    import asyncio
    from datamaxi.aio import AsyncDatamaxi


    async def main():
        async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
            exchanges = await client.cex.candle.exchanges(market="spot")
            symbols = await client.cex.candle.symbols(exchange="binance", market="spot")
            intervals = await client.cex.candle.intervals()

            df = await client.cex.candle(
                exchange="binance",
                symbol="BTC-USDT",
                interval="1d",
                market="spot",
                from_unix=1704067200,
                to_unix=1706745600,
            )


    asyncio.run(main())
    ```

## Notes

- `from_unix` and `to_unix` use Unix timestamps in seconds.
- Set `pandas=False` to return the raw dict response.

::: datamaxi.resources.CexCandle
    options:
      show_submodules: true
      show_source: false
