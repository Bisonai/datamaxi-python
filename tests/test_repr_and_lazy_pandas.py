"""Tests for the #143 polish: __repr__ and lazy pandas import."""

import subprocess
import sys

from datamaxi import Datamaxi
from datamaxi.api import API

BASE_URL = "https://api.datamaxiplus.com"


def test_api_repr():
    r = repr(API(api_key="secret", base_url=BASE_URL))
    assert r == "API(base_url='https://api.datamaxiplus.com', has_key=True)"
    assert "secret" not in r


def test_resource_repr_uses_class_name():
    c = Datamaxi(api_key="secret", base_url=BASE_URL)
    assert repr(c.cex) == "Cex(base_url='https://api.datamaxiplus.com', has_key=True)"
    assert (
        repr(c.cex.candle)
        == "CexCandle(base_url='https://api.datamaxiplus.com', has_key=True)"
    )
    assert "secret" not in repr(c.cex.candle)


def test_datamaxi_repr_and_no_key_leak(monkeypatch):
    c = Datamaxi(api_key="secret", base_url=BASE_URL)
    assert repr(c) == "Datamaxi(base_url='https://api.datamaxiplus.com', has_key=True)"
    assert "secret" not in repr(c)
    # has_key=False only holds with no key from arg *or* environment
    monkeypatch.delenv("DATAMAXI_API_KEY", raising=False)
    assert "has_key=False" in repr(Datamaxi(base_url=BASE_URL))


def test_importing_datamaxi_does_not_load_pandas():
    # Isolated subprocess: other tests in this session load pandas, so a
    # same-process sys.modules check would be unreliable.
    code = "import sys, datamaxi; " "sys.exit(0 if 'pandas' not in sys.modules else 1)"
    result = subprocess.run([sys.executable, "-c", code])
    assert result.returncode == 0, "importing datamaxi should not import pandas"
