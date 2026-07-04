# Naver Trend

Search trend data for South Korea via Naver.

## Usage

=== "Sync"

    ```python
    from datamaxi import Naver

    naver = Naver(api_key="YOUR_API_KEY")

    symbols = naver.symbols()
    trend = naver.trend(symbol="BTC")
    ```

=== "Async"

    ```python
    import asyncio
    from datamaxi.aio import AsyncNaver


    async def main():
        async with AsyncNaver(api_key="YOUR_API_KEY") as naver:
            symbols = await naver.symbols()
            trend = await naver.trend(symbol="BTC")


    asyncio.run(main())
    ```

## Notes

- Set `pandas=False` to return the raw list response.

::: datamaxi.naver
    options:
      show_submodules: true
      show_source: false
