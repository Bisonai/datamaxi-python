import os
import json
from json import JSONDecodeError
import logging
import requests
from .__version__ import __version__
from datamaxi.error import ClientError, ServerError
from datamaxi.lib.utils import cleanNoneValue
from datamaxi.lib.utils import encoded_string
from datamaxi.lib.utils import check_required_parameter
from datamaxi._endpoints import ENDPOINTS


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
    ):
        """Client API constructor. `api_key` can be set
        as an environment variable `DATAMAXI_API_KEY`.

        Args:
            api_key (str): The API key for the DataMaxi+ API.
            base_url (str): The base URL for the DataMaxi+ API.
            timeout (int): The timeout for the requests.
            proxies (dict): The proxies for the requests.
            show_limit_usage (bool): Show the limit usage.
            show_header (bool): Show the header.
        """
        self.api_key = api_key or os.environ.get("DATAMAXI_API_KEY")
        self.base_url = base_url
        self.timeout = timeout
        self.proxies = proxies if type(proxies) is dict else None
        self.show_limit_usage = bool(show_limit_usage)
        self.show_header = bool(show_header)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "User-Agent": "datamaxi/" + __version__,
                "X-DTMX-APIKEY": str(self.api_key),
            }
        )

        self._logger = logging.getLogger(__name__)
        return

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
        """
        ep = ENDPOINTS.get(op_id)
        if ep is None:
            raise ValueError(f"unknown endpoint operation_id: {op_id!r}")

        spec_params = ep.get("params", {})

        unknown = set(params) - set(spec_params)
        if unknown:
            raise ValueError(
                f"{op_id}: unknown parameter(s) {sorted(unknown)}; "
                f"expected one of {sorted(spec_params)}"
            )

        # Resolve each value: caller-supplied, else the registry default.
        values = {}
        for name, meta in spec_params.items():
            val = params.get(name)
            if val is None and "default" in meta:
                val = meta["default"]
            values[name] = val

        # Enforce params the spec marks required.
        for name, meta in spec_params.items():
            if meta.get("required"):
                check_required_parameter(values.get(name), name)

        # Split path vs query params; interpolate path params into the URL.
        url_path = ep["path"]
        query_params = {}
        for name, meta in spec_params.items():
            if meta.get("in") == "path":
                url_path = url_path.replace("{" + name + "}", str(values[name]))
            else:
                query_params[name] = values[name]

        return self.send_request(ep["method"], url_path, payload=query_params)

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
        result = {}

        if self.show_limit_usage:
            limit_usage = {}
            for key in response.headers.keys():
                key = key.lower()
                if (
                    key.startswith("x-ratelimit-limit")
                    or key.startswith("x-ratelimit-remaining")
                    or key.startswith("x-ratelimit-reset")
                ):
                    limit_usage[key] = response.headers[key]
            result["limit_usage"] = limit_usage

        if self.show_header:
            result["header"] = response.headers

        if len(result) != 0:
            result["data"] = data
            return result

        return data

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
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, response.text, None, response.headers)
            error_data = None
            if "data" in err:
                error_data = err["data"]
            raise ClientError(
                status_code,
                err["error"],
                response.headers,
                error_data,
            )
        raise ServerError(status_code, response.text)
