# Telegram

Telegram channel metadata and message history.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Datamaxi

telegram = Datamaxi(api_key="YOUR_API_KEY").telegram

channels, _ = telegram.channels(category="korean", limit=50)
messages, next_request = telegram.messages(channel_name="yunlog_announcement", limit=50)

more_messages, _ = next_request()
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncDatamaxi


async def main():
    async with AsyncDatamaxi(api_key="YOUR_API_KEY") as client:
        channels, _ = await client.telegram.channels(category="korean", limit=50)
        messages, next_request = await client.telegram.messages(
            channel_name="yunlog_announcement", limit=50
        )

        more_messages, _ = await next_request()


asyncio.run(main())
```

</details>

## Notes

- Pagination returns a `next_request` function for the next page.
- Example uses `category="korean"` from the live channels list.

::: datamaxi.telegram
    options:
      show_submodules: true
      show_source: false
