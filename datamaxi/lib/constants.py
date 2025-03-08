from typing import Final

BASE_URL: Final = "https://api.datamaxiplus.com"
SPOT: Final = "spot"
FUTURES: Final = "futures"
USD: Final = "USD"

INTERVAL_1M: Final = "1m"
INTERVAL_5M: Final = "5m"
INTERVAL_15M: Final = "15m"
INTERVAL_30M: Final = "30m"
INTERVAL_1H: Final = "1h"
INTERVAL_4H: Final = "4h"
INTERVAL_12H: Final = "12h"
INTERVAL_1D: Final = "1d"

SUPPORTED_INTERVALS: Final = [
    INTERVAL_1M,
    INTERVAL_5M,
    INTERVAL_15M,
    INTERVAL_30M,
    INTERVAL_1H,
    INTERVAL_4H,
    INTERVAL_12H,
    INTERVAL_1D,
]

ASC: Final = "asc"
DESC: Final = "desc"
