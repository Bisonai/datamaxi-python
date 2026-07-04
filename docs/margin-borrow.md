# Margin Borrow

Margin borrow data for a single asset.

## Usage

=== "Sync"

    ```python
    from datamaxi import Datamaxi

    maxi = Datamaxi(api_key="YOUR_API_KEY")

    data = maxi.margin_borrow(asset="BTC")
    ```

=== "Async"

    ```python
    import asyncio
    from datamaxi.aio import AsyncDatamaxi


    async def main():
        async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
            data = await client.margin_borrow(asset="BTC")


    asyncio.run(main())
    ```

::: datamaxi.resources.MarginBorrow
    options:
      show_submodules: true
      show_source: false
