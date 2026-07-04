# Funding Rate

Historical and latest funding rates for perpetual futures.

## Usage

=== "Sync"

    ```python
    from datamaxi import Datamaxi

    maxi = Datamaxi(api_key="YOUR_API_KEY")

    exchanges = maxi.funding_rate.exchanges()
    symbols = maxi.funding_rate.symbols(exchange="binance")

    history, next_request = maxi.funding_rate.history(
        exchange="binance",
        symbol="BTC-USDT",
        page=1,
        limit=100,
        sort="desc",
    )

    latest = maxi.funding_rate.latest(exchange="binance", symbol="BTC-USDT")
    ```

=== "Async"

    ```python
    import asyncio
    from datamaxi.aio import AsyncDatamaxi


    async def main():
        async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
            exchanges = await client.funding_rate.exchanges()
            symbols = await client.funding_rate.symbols(exchange="binance")

            history, next_request = await client.funding_rate.history(
                exchange="binance",
                symbol="BTC-USDT",
                page=1,
                limit=100,
                sort="desc",
            )

            latest = await client.funding_rate.latest(exchange="binance", symbol="BTC-USDT")


    asyncio.run(main())
    ```

## Notes

- Pagination returns a `next_request` function for the next page.
- Set `pandas=False` to return the raw dict response.

::: datamaxi.resources.FundingRate
    options:
      show_submodules: true
      show_source: false
