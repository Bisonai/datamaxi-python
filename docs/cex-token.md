# CEX Token

Token listing and delisting updates from centralized exchanges.

## Usage

=== "Sync"

    ```python
    from datamaxi import Datamaxi

    maxi = Datamaxi(api_key="YOUR_API_KEY")

    data, next_request = maxi.cex.token.updates(
        type="listed",
        page=1,
        limit=100,
    )

    more_data, _ = next_request()
    ```

=== "Async"

    ```python
    import asyncio
    from datamaxi.aio import AsyncDatamaxi


    async def main():
        async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
            data, next_request = await client.cex.token.updates(
                type="listed",
                page=1,
                limit=100,
            )

            more_data, _ = await next_request()


    asyncio.run(main())
    ```

## Notes

- Use `type="listed"` or `type="delisted"` to filter update types.

::: datamaxi.resources.CexToken
    options:
      show_submodules: true
      show_source: false
