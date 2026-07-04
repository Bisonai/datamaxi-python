"""Transport-agnostic request helpers shared by the sync and async clients.

Keeping the endpoint resolution and error handling here (rather than in
``API``) lets the ``httpx``-based async client reuse exactly the same
param-splitting and error semantics as the sync ``requests`` client, so the
two can't drift.
"""

import json
from json import JSONDecodeError

from datamaxi.error import ClientError, ServerError
from datamaxi.lib.utils import check_required_parameter
from datamaxi._endpoints import ENDPOINTS


def resolve_endpoint(op_id, **params):
    """Resolve ``op_id`` + caller params into ``(method, url_path, query)``.

    Uses ``datamaxi._endpoints.ENDPOINTS`` (generated from the backend
    OpenAPI spec) as the single source of truth for path, method, the
    path/query split, required params, and defaults.
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

    return ep["method"], url_path, query_params


def raise_for_error(status_code, text, headers):
    """Raise ``ClientError`` / ``ServerError`` for a 4xx / 5xx response.

    Works on any response given its ``status_code`` / ``text`` / ``headers``,
    so it applies identically to ``requests`` and ``httpx`` responses.
    """
    if status_code < 400:
        return
    if 400 <= status_code < 500:
        try:
            err = json.loads(text)
        except JSONDecodeError:
            raise ClientError(status_code, text, None, headers) from None
        error_data = None
        if "data" in err:
            error_data = err["data"]
        raise ClientError(status_code, err.get("error", text), headers, error_data)
    raise ServerError(status_code, text)


def extract_limit_usage(headers):
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
