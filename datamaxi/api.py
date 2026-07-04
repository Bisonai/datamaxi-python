import os
import logging
import warnings
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .__version__ import __version__
from datamaxi.lib.utils import cleanNoneValue
from datamaxi.lib.utils import encoded_string
from datamaxi._dispatch import resolve_endpoint, raise_for_error


class API(object):
    """The base class for all DataMaxi+ Python clients. `api_key` can be set
    as an environment variable `DATAMAXI_API_KEY`.
    """

    def __init__(
        self,
        api_key=None,
        base_url=None,
        timeout=10,
        proxies=None,
        show_limit_usage=False,
        show_header=False,
        max_retries=3,
        retry_backoff=0.5,
        retry_statuses=(502, 503, 504),
    ):
        """Client API constructor. `api_key` can be set
        as an environment variable `DATAMAXI_API_KEY`.

        Args:
            api_key (str): The API key for the DataMaxi+ API.
            base_url (str): The base URL for the DataMaxi+ API.
            timeout (int): The timeout for the requests.
            proxies (dict): The proxies for the requests.
            show_limit_usage (bool): Deprecated. Metadata is now always
                available via ``last_response``; this flag no longer changes
                the return shape. Kept for backward compatibility.
            show_header (bool): Deprecated. See ``show_limit_usage`` /
                ``last_response``.
            max_retries (int): Retry attempts for transient gateway 5xx
                and connection/read errors. Set to 0 to disable.
            retry_backoff (float): Backoff factor between retries (seconds);
                see urllib3 ``Retry(backoff_factor=...)``.
            retry_statuses (tuple): HTTP status codes treated as transient
                and retried (GET only).
        """
        self.api_key = api_key or os.environ.get("DATAMAXI_API_KEY")
        self.base_url = base_url
        self.timeout = timeout
        self.proxies = proxies if type(proxies) is dict else None
        self.show_limit_usage = bool(show_limit_usage)
        self.show_header = bool(show_header)
        for _flag, _name in (
            (show_limit_usage, "show_limit_usage"),
            (show_header, "show_header"),
        ):
            if _flag:
                warnings.warn(
                    "'{}' is deprecated and no longer changes the return "
                    "shape; read response metadata from "
                    "`client.<resource>.last_response` instead. It will be "
                    "removed in a future major release.".format(_name),
                    DeprecationWarning,
                    stacklevel=2,
                )
        # Metadata for the most recent successful response (see #140).
        # Populated on every call; None until the first request.
        self.last_response = None

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "datamaxi/" + __version__,
                "X-DTMX-APIKEY": str(self.api_key),
            }
        )
        self._mount_retries(max_retries, retry_backoff, retry_statuses)

        self._logger = logging.getLogger(__name__)
        return

    def _mount_retries(self, max_retries, retry_backoff, retry_statuses):
        """Mount a urllib3 retry policy on the session's HTTP adapters.

        Retries transient gateway 5xx (``retry_statuses``) and
        connection/read failures on idempotent GETs, honoring any
        ``Retry-After`` header. ``raise_on_status`` is False so an
        exhausted retry returns the final response and the SDK's own
        ``_handle_exception`` still raises ``ServerError`` — preserving
        the existing error contract instead of leaking urllib3's
        ``MaxRetryError``.
        """
        retry = Retry(
            total=max_retries,
            connect=max_retries,
            read=max_retries,
            status=max_retries,
            status_forcelist=tuple(retry_statuses),
            allowed_methods=frozenset(["GET"]),
            backoff_factor=retry_backoff,
            respect_retry_after_header=True,
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def __repr__(self):
        return "{}(base_url={!r}, has_key={})".format(
            type(self).__name__, self.base_url, bool(self.api_key)
        )

    def close(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def query(self, url_path, payload=None):
        return self.send_request("GET", url_path, payload=payload)

    def request_endpoint(self, op_id, **params):
        """Dispatch a request described by the generated endpoint registry.

        Looks up ``op_id`` in ``datamaxi._endpoints.ENDPOINTS`` (regenerated
        from the backend OpenAPI spec by datamaxi-codegen) and uses it as the
        single source of truth for the URL path, HTTP method, path/query split,
        required params, and default values. Callers pass wire-level parameter
        names as keyword arguments (e.g. ``**{"from": from_unix}``); semantic
        validation and response shaping stay in the calling client method.

        The resolution itself lives in ``datamaxi._dispatch.resolve_endpoint``
        so the async client reuses identical param handling.
        """
        method, url_path, query_params = resolve_endpoint(op_id, **params)
        return self.send_request(method, url_path, payload=query_params)

    def send_request(self, http_method, url_path, payload=None):
        if payload is None:
            payload = {}
        url = self.base_url + url_path
        self._logger.debug("url: " + url)
        params = cleanNoneValue(
            {
                "url": url,
                "params": self._prepare_params(payload),
                "timeout": self.timeout,
                "proxies": self.proxies,
            }
        )
        response = self._dispatch_request(http_method)(**params)
        self._logger.debug("raw response from server:" + response.text)
        self._handle_exception(response)

        try:
            data = response.json()
        except ValueError:
            data = response.text

        # Always expose response metadata via last_response instead of
        # wrapping it into the return value. The old wrapper keyed rate-limit
        # info under "data" too, which collided with the backend's own
        # ``{"data": ...}`` envelope and corrupted the DataFrame code paths.
        self.last_response = ResponseMeta(
            status_code=response.status_code,
            headers=response.headers,
            limit_usage=self._extract_limit_usage(response.headers),
            data=data,
        )

        return data

    @staticmethod
    def _extract_limit_usage(headers):
        """Pull the ``x-ratelimit-*`` triplet out of the response headers."""
        usage = {}
        for key in headers.keys():
            k = key.lower()
            if (
                k.startswith("x-ratelimit-limit")
                or k.startswith("x-ratelimit-remaining")
                or k.startswith("x-ratelimit-reset")
            ):
                usage[k] = headers[key]
        return usage

    def _prepare_params(self, params):
        return encoded_string(cleanNoneValue(params))

    def _dispatch_request(self, http_method):
        return {
            "GET": self.session.get,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
            "POST": self.session.post,
        }.get(http_method, "GET")

    def _handle_exception(self, response):
        raise_for_error(response.status_code, response.text, response.headers)


class ResponseMeta(object):
    """Metadata for the most recent successful response.

    Exposed via ``client.<resource>.last_response`` so per-call info
    (rate-limit usage, headers, status) no longer has to be wrapped into —
    and change the shape of — the returned payload. The client tree shares
    one transport, so this reflects the *last* call made through it.
    """

    __slots__ = ("status_code", "headers", "limit_usage", "data")

    def __init__(self, status_code, headers, limit_usage, data):
        self.status_code = status_code
        self.headers = headers
        self.limit_usage = limit_usage
        self.data = data

    def __repr__(self):
        return "ResponseMeta(status_code={}, limit_usage={})".format(
            self.status_code, self.limit_usage
        )


class Resource(object):
    """Base for endpoint/resource clients — *composes* an `API` transport
    rather than subclassing it.

    Every resource holds a shared `API` (one `requests.Session` /
    connection pool) instead of each opening its own. A resource either
    receives an already-built ``api`` (the normal path — `Datamaxi`
    constructs one and threads it through the whole tree via ``**kwargs``)
    or builds its own from ``api_key``/``**kwargs`` for direct, standalone
    instantiation. The thin `request_endpoint`/`query` forwarders keep the
    call sites in the resource methods unchanged (`self.request_endpoint(...)`).
    """

    def __init__(self, api_key=None, api=None, **kwargs):
        self._api = api if api is not None else API(api_key, **kwargs)

    def __repr__(self):
        return "{}(base_url={!r}, has_key={})".format(
            type(self).__name__, self._api.base_url, bool(self._api.api_key)
        )

    def request_endpoint(self, op_id, **params):
        return self._api.request_endpoint(op_id, **params)

    def query(self, url_path, payload=None):
        return self._api.query(url_path, payload=payload)

    @property
    def last_response(self):
        """`ResponseMeta` for the most recent call through the shared transport."""
        return self._api.last_response
