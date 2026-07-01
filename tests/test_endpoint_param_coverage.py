"""Reproducible audit: every registry param is reachable from the SDK.

``datamaxi/_endpoints.py`` is the codegen registry mirroring the live backend
OpenAPI contract (data-api routes only; front-api ``/api/v1/front/*`` is
excluded from the spec). Client methods dispatch through
``API.request_endpoint(op_id, **params)`` — so a registry-declared param is
only reachable if some client call site forwards it as a keyword argument.

This test statically extracts, per ``op_id``, the union of keyword arguments
forwarded at every ``request_endpoint("op_id", ...)`` call site (handling the
``**{"from": ...}`` dict-splat and the ``**params`` local-dict patterns), then
asserts that every registry param is either forwarded, globally ignored
(pagination), or explicitly allow-listed below with a rationale.

Regenerating ``_endpoints.py`` (``make python`` upstream) that adds a new param
to any endpoint will fail this test until the client method forwards it or it
is allow-listed here — that is the point: it catches silent drift.

Issue #123.
"""

import ast
import os

import datamaxi
from datamaxi._endpoints import ENDPOINTS

# Pagination is handled per-method (some methods expose page/limit and their
# own next_request pager, aggregate endpoints return the raw page). The issue
# scopes the audit to non-pagination params, so ignore these globally.
_IGNORED_PARAMS = {"page", "limit"}


# Registry params intentionally NOT reachable from the SDK yet, with rationale.
# Shape: {op_id: {param_name: "why"}}. Only the params listed for an op_id are
# allow-listed, so to exempt a whole endpoint every one of its params must be
# named here (an empty dict exempts nothing).
#
# NOTE FOR HUMAN REVIEW: #126 exposed index_price, margin_borrow, and
# liquidation_stats with dedicated client methods (they are no longer here).
# listings_historical remains intentionally SDK-excluded — its param is
# allow-listed below with that rationale.
_ALLOWLIST = {
    # Intentionally SDK-excluded (#126): not surfaced in the public data-api.
    "listings_historical": {
        "refresh": "intentionally SDK-excluded — not surfaced in the public "
        "data-api (see #126)",
    },
}


def _iter_py_files(pkg_dir):
    for root, _dirs, files in os.walk(pkg_dir):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            if fn in ("_endpoints.py", "api.py"):
                # _endpoints.py is the registry itself; api.py defines the
                # generic dispatcher, not per-endpoint call sites.
                continue
            yield os.path.join(root, fn)


def _enclosing_func(parents, node):
    cur = node
    while cur is not None:
        cur = parents.get(cur)
        if isinstance(cur, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return cur
    return None


def _subscript_string_keys(func_node, name):
    """Collect literal keys of ``name[<str>] = ...`` assignments in ``func``."""
    keys = set()
    if func_node is None:
        return keys
    for n in ast.walk(func_node):
        if not isinstance(n, ast.Assign):
            continue
        for tgt in n.targets:
            if (
                isinstance(tgt, ast.Subscript)
                and isinstance(tgt.value, ast.Name)
                and tgt.value.id == name
                and isinstance(tgt.slice, ast.Constant)
                and isinstance(tgt.slice.value, str)
            ):
                keys.add(tgt.slice.value)
    return keys


def _is_request_endpoint_call(node):
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "request_endpoint"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
    )


def _forwarded_names_of_call(node, parents):
    """Param names a single ``request_endpoint(...)`` call forwards."""
    names = set()
    for kw in node.keywords:
        if kw.arg is not None:
            names.add(kw.arg)
        elif isinstance(kw.value, ast.Dict):
            # request_endpoint(op, **{"from": x, "to": y})
            for key in kw.value.keys:
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    names.add(key.value)
        elif isinstance(kw.value, ast.Name):
            # request_endpoint(op, **params) — resolve params[...] = ...
            func = _enclosing_func(parents, node)
            names |= _subscript_string_keys(func, kw.value.id)
    return names


def _collect_forwarded_params():
    """Map ``op_id`` -> set of param names forwarded by any client call site.

    Endpoints with no call site at all are absent from the returned mapping.
    """
    pkg_dir = os.path.dirname(datamaxi.__file__)
    forwarded = {}

    for path in _iter_py_files(pkg_dir):
        with open(path, "r", encoding="utf-8") as fh:
            tree = ast.parse(fh.read(), path)

        parents = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent

        for node in ast.walk(tree):
            if not _is_request_endpoint_call(node):
                continue
            op_id = node.args[0].value
            forwarded.setdefault(op_id, set()).update(
                _forwarded_names_of_call(node, parents)
            )

    return forwarded


def test_audit_extraction_sees_known_call_sites():
    """Guardrail: the AST extractor actually resolves the tricky patterns.

    If these regress (e.g. extractor stops resolving ``**params``), the main
    audit could pass vacuously — pin the two non-trivial patterns here.
    """
    forwarded = _collect_forwarded_params()
    # premium uses the **params local-dict pattern.
    assert "query" in forwarded.get("premium", set())
    assert "source_exchange" in forwarded.get("premium", set())
    # open_interest history-aggregated uses the **{"from": ...} splat.
    assert "from" in forwarded.get("open_interest_history_aggregated", set())


def test_allowlist_has_no_stale_entries():
    """Allow-listed params must still exist in the registry (no dead entries)."""
    for op_id, params in _ALLOWLIST.items():
        assert op_id in ENDPOINTS, f"allowlist op_id {op_id!r} not in registry"
        reg = set(ENDPOINTS[op_id].get("params", {}))
        stale = set(params) - reg
        assert not stale, f"{op_id}: allowlist params no longer in registry: {stale}"


def test_every_registry_param_is_exposed_or_allowlisted():
    """Every registry param is forwarded by the SDK, ignored, or allow-listed."""
    forwarded = _collect_forwarded_params()
    unreachable = {}

    for op_id, ep in ENDPOINTS.items():
        reg = set(ep.get("params", {}))
        exposed = forwarded.get(op_id, set())
        allowed = set(_ALLOWLIST.get(op_id, {}))
        missing = reg - exposed - _IGNORED_PARAMS - allowed
        if missing:
            unreachable[op_id] = sorted(missing)

    assert not unreachable, (
        "Registry params not reachable from the SDK (expose them in the client "
        "method or add to _ALLOWLIST with a rationale):\n"
        + "\n".join(f"  {op}: {params}" for op, params in sorted(unreachable.items()))
    )
