"""Shared transient-5xx retry policy for the sync and async transports.

The sync client (``datamaxi.api.API``) mounts a ``urllib3.util.retry.Retry``
on its ``requests.Session`` adapters, which already implements this policy
for `requests`. The async client (``datamaxi.aio._core.AsyncAPI``) is built
on ``httpx``, which has no equivalent adapter-level retry, so it hand-rolls
its own loop. This module is the single description of that policy so the
two loops can't drift onto different retry behavior:

* GET-only — retries are only safe for idempotent requests.
* Exponential backoff — mirrors ``Retry.get_backoff_time()``: no delay
  before the first retry, then ``backoff_factor * 2 ** (n - 1)`` before the
  n-th retry (n >= 2), capped at ``BACKOFF_MAX`` seconds.
* Honors a ``Retry-After`` response header (seconds or HTTP-date form) when
  present, taking priority over the computed backoff — mirrors
  ``Retry.respect_retry_after_header=True``.
"""

import email.utils
import re
import time

#: Matches urllib3's ``Retry.DEFAULT_BACKOFF_MAX``.
BACKOFF_MAX = 120.0

_RETRY_AFTER_SECONDS_RE = re.compile(r"^\s*[0-9]+\s*$")


def is_retryable(method, status_code, attempt, max_retries, retry_statuses):
    """Whether attempt number ``attempt`` (1 = first failure) may be retried.

    Only idempotent GETs are retried, only for statuses in
    ``retry_statuses``, and only while ``attempt <= max_retries``.
    """
    return (
        str(method).upper() == "GET"
        and status_code in retry_statuses
        and attempt <= max_retries
    )


def parse_retry_after(value):
    """Parse a ``Retry-After`` header value into seconds, or ``None``.

    Accepts either the numeric-seconds form or an HTTP-date, matching
    ``urllib3.util.retry.Retry.parse_retry_after``. Returns ``None`` if
    ``value`` is ``None`` or not parseable; never returns a negative number.
    """
    if value is None:
        return None

    if _RETRY_AFTER_SECONDS_RE.match(value):
        seconds = float(value)
    else:
        retry_date_tuple = email.utils.parsedate_tz(value)
        if retry_date_tuple is None:
            return None
        if retry_date_tuple[9] is None:
            retry_date_tuple = retry_date_tuple[:9] + (0,) + retry_date_tuple[10:]
        retry_date = email.utils.mktime_tz(retry_date_tuple)
        seconds = retry_date - time.time()

    return max(0.0, seconds)


def get_backoff_time(attempt, backoff_factor):
    """Seconds to sleep before retry number ``attempt`` (1 = first retry).

    Matches urllib3's ``Retry.get_backoff_time()``: zero delay before the
    first retry, then exponential growth, capped at ``BACKOFF_MAX``.
    """
    if attempt <= 1:
        return 0.0
    return min(BACKOFF_MAX, backoff_factor * (2 ** (attempt - 1)))


def get_retry_delay(attempt, backoff_factor, headers):
    """Seconds to sleep before retry number ``attempt``, honoring ``Retry-After``.

    ``headers`` is any mapping-like object exposing ``.get(...)``
    (``requests``/``httpx`` headers are both case-insensitive mappings).
    """
    retry_after = parse_retry_after(headers.get("Retry-After"))
    if retry_after is not None:
        return retry_after
    return get_backoff_time(attempt, backoff_factor)
