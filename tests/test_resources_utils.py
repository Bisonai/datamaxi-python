"""Tests for the shared response-shaping helpers (``datamaxi.resources.utils``,
see #154) — param assembly, the "no data" check, and DataFrame shaping used
by both the sync and async resources.
"""

import pandas as pd
import pytest

from datamaxi.resources.utils import (
    assemble_params,
    raise_if_no_data,
    to_indexed_dataframe,
)


def test_assemble_params_drops_none_and_keeps_order():
    params = assemble_params(
        ("a", 1),
        ("b", None),
        ("c", "x"),
    )
    assert params == {"a": 1, "c": "x"}
    assert list(params) == ["a", "c"]


def test_assemble_params_only_truthy_flag_pattern():
    # Call-site pattern for "include only if truthy" flags like
    # only_transferable: pass `True if flag else None`.
    included = assemble_params(("only_transferable", True if True else None))
    excluded = assemble_params(("only_transferable", True if False else None))
    assert included == {"only_transferable": True}
    assert excluded == {}


def test_raise_if_no_data_raises_on_none():
    with pytest.raises(ValueError):
        raise_if_no_data({"data": None})


def test_raise_if_no_data_raises_on_empty_by_default():
    with pytest.raises(ValueError):
        raise_if_no_data({"data": []})


def test_raise_if_no_data_allows_empty_when_length_check_disabled():
    raise_if_no_data({"data": []}, check_length=False)  # no raise


def test_raise_if_no_data_passes_with_data():
    raise_if_no_data({"data": [{"x": 1}]})


def test_to_indexed_dataframe_single_row():
    df = to_indexed_dataframe([{"d": "123", "p": "1.5"}], "d")
    assert isinstance(df, pd.DataFrame)
    assert df.index.name == "d"
    assert list(df.index) == ["123"]


def test_to_indexed_dataframe_multi_row():
    df = to_indexed_dataframe(
        [{"network": "BSC", "x": 1}, {"network": "ETH", "x": 2}], "network"
    )
    assert list(df.index) == ["BSC", "ETH"]
