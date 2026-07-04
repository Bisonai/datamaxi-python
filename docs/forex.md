# Forex

Foreign exchange spot rates.

## Usage

=== "Sync"

    ```python
    from datamaxi import Datamaxi

    maxi = Datamaxi(api_key="YOUR_API_KEY")

    symbols = maxi.forex.symbols()
    data = maxi.forex(symbol="USD-KRW")
    ```

=== "Async"

    ```python
    import asyncio
    from datamaxi.aio import AsyncDatamaxi


    async def main():
        async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
            symbols = await client.forex.symbols()
            data = await client.forex(symbol="USD-KRW")


    asyncio.run(main())
    ```

## Notes

- Set `pandas=False` to return the raw dict response.

::: datamaxi.resources.Forex
    options:
      show_submodules: true
      show_source: false
