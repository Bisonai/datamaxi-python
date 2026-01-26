# Telegram

Telegram channel metadata and message history.

## Usage

```python
from datamaxi import Telegram

telegram = Telegram(api_key="YOUR_API_KEY")

channels, _ = telegram.channels(category="korean", limit=50)
messages, next_request = telegram.messages(channel_name="yunlog_announcement", limit=50)

more_messages, _ = next_request()
```

## Notes

- Pagination returns a `next_request` function for the next page.
- Example uses `category="korean"` from the live channels list.

::: datamaxi.telegram
    options:
      show_submodules: true
      show_source: false
