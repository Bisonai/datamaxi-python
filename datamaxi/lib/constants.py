from typing import Final, Literal

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

# Type aliases for the enumerable string parameters used across the client
# surface. These are hint-only (Literal is not enforced at runtime), so
# passing a bare string still works — they exist to give IDE/mypy checking.
Market = Literal["spot", "futures"]
Interval = Literal["1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d"]
SortOrder = Literal["asc", "desc"]
