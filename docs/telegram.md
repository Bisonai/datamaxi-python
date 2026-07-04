# Telegram

Telegram channel metadata and message history.

## Usage

<details markdown="1"><summary>Sync</summary>

```python
from datamaxi import Telegram

telegram = Telegram(api_key="YOUR_API_KEY")

channels, _ = telegram.channels(category="korean", limit=50)
messages, next_request = telegram.messages(channel_name="yunlog_announcement", limit=50)

more_messages, _ = next_request()
```

</details>

<details markdown="1"><summary>Async</summary>

```python
import asyncio
from datamaxi.aio import AsyncTelegram


async def main():
    async with AsyncTelegram(api_key="YOUR_API_KEY") as telegram:
        channels, _ = await telegram.channels(category="korean", limit=50)
        messages, next_request = await telegram.messages(
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
