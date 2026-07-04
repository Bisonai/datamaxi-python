"""Transport-agnostic response-shaping helpers shared by the sync and async
resources (see #154).

Kept alongside ``datamaxi._dispatch`` (which shares *request*-building) as
the shared *response*-shaping layer: param assembly, the "no data" envelope
check, and the DataFrame-vs-raw-dict conversion decision. Pure functions
only (deferred ``pandas`` import, no ``requests``/``httpx``), so both
``datamaxi.resources.*`` and ``datamaxi.aio.*`` can import this leaf module
without any import-cycle risk.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def assemble_params(*pairs: Tuple[str, Any]) -> Dict[str, Any]:
    """Build a query-param dict from ``(name, value)`` pairs, dropping ``None``.

    Mirrors the repeated ``if x is not None: params["x"] = x`` blocks that
    were hand-copied across sync/async resource methods. For "only include
    when truthy" flags (e.g. ``only_transferable``), pass ``value if value
    else None`` at the call site.
    """
    return {name: value for name, value in pairs if value is not None}


def raise_if_no_data(res: Dict[str, Any], check_length: bool = True) -> None:
    """Raise ``ValueError("no data found")`` for an empty ``{"data": ...}`` envelope.

    ``check_length`` matches call sites that also treat an empty
    list/dict as "no data" (e.g. candle, premium), vs. ones that only
    check for ``None`` (e.g. announcements, token updates).
    """
    if res["data"] is None or (check_length and len(res["data"]) == 0):
        raise ValueError("no data found")


def to_indexed_dataframe(rows: List, index_col: str) -> pd.DataFrame:
    """``pd.DataFrame(rows).set_index(index_col)`` — the ticker/wallet-status shape.

    ``rows`` is already a list of dicts (wrap a single dict as ``[rows]`` at
    the call site, as the ticker endpoint's bare-object response does).
    """
    import pandas as pd

    df = pd.DataFrame(rows)
    df = df.set_index(index_col)
    return df


def convert_data_to_data_frame(
    data: List,
    columns_to_replace: List[str] = [],
) -> pd.DataFrame:
    import pandas as pd

    df = pd.DataFrame(data)
    df = df.set_index("d")

    if len(columns_to_replace) == 0:
        df.replace("NaN", pd.NA, inplace=True)
        df = df.apply(pd.to_numeric, errors="coerce")
        return df

    df[columns_to_replace] = df[columns_to_replace].replace("NaN", pd.NA)
    df[columns_to_replace] = df[columns_to_replace].apply(
        pd.to_numeric, errors="coerce"
    )

    return df
