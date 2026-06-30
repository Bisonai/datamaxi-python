"""Unit tests for datamaxi.error exception classes. No API key / network."""

from datamaxi.error import (
    Error,
    ClientError,
    ServerError,
    ParameterRequiredError,
    AtLeastOneParameterRequiredError,
)


def test_client_error_stores_fields():
    err = ClientError(400, "bad request", {"h": "1"}, error_data={"code": -1})
    assert isinstance(err, Error)
    assert err.status_code == 400
    assert err.error_message == "bad request"
    assert err.header == {"h": "1"}
    assert err.error_data == {"code": -1}


def test_client_error_error_data_defaults_none():
    err = ClientError(404, "not found", {})
    assert err.error_data is None


def test_server_error_stores_fields():
    err = ServerError(500, "no data found")
    assert isinstance(err, Error)
    assert err.status_code == 500
    assert err.message == "no data found"


def test_parameter_required_error_message():
    err = ParameterRequiredError(["exchange", "symbol"])
    assert str(err) == "exchange, symbol is mandatory, but received empty."


def test_at_least_one_parameter_required_error_message():
    assert (
        str(AtLeastOneParameterRequiredError()) == "At least one parameter is required."
    )
