import os
import pytest
from unittest.mock import patch

from app.exceptions import MissingEnvironmentVariableError
from app.utils import (
    load_environment_variable,
    get_environment_variables,
    get_db_credentials,
    get_query_parameters,
    get_formatted_flux_query,
)


def test_load_environment_variable():
    key, value = "FOO", "BAR"

    with patch.dict(os.environ, {key: value}):
        var = load_environment_variable(key)
        assert var == value


def test_load_missing_environment_variable():
    with pytest.raises(MissingEnvironmentVariableError):
        load_environment_variable("MISSING")


def test_get_environment_variables():
    env_vars = {"ONE": "1", "TWO": "2"}
    with patch.dict(os.environ, env_vars):
        ret = get_environment_variables(env_vars.keys())
        assert ret == env_vars


def test_get_db_credentials():
    env_vars = {
        "INFLUXDB_HOST": "influxdb",
        "INFLUXDB_PORT": "8086",
        "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN": "mocked-token",
        "DOCKER_INFLUXDB_INIT_ORG": "mocked-org",
    }

    ret = get_db_credentials(env_vars)

    assert ret["org"] == env_vars["DOCKER_INFLUXDB_INIT_ORG"]
    assert ret["token"] == env_vars["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
    assert (
        ret["url"] == f"http://{env_vars['INFLUXDB_HOST']}:{env_vars['INFLUXDB_PORT']}"
    )


def test_get_query_parameters():
    device_id = "sensor-1"
    start = "2020-01-02T03:44:00"
    stop = "2020-01-02T03:45:00"

    ret = get_query_parameters(device_id, start, stop)

    assert ret["deviceId"] == device_id
    assert ret["start"] == start
    assert ret["stop"] == stop


def test_get_formatted_flux_query():
    bucket = "test_bucket"
    query_parameters = {
        "deviceId": "sensor-1",
        "start": "2020-01-02T03:44:00",
        "stop": "2020-01-02T03:45:00",
    }

    ret = get_formatted_flux_query(bucket, query_parameters)
    assert ret == (
        ' from(bucket:"test_bucket")'
        " |> range(start: 2020-01-02T03:44:00Z, stop: 2020-01-02T03:45:00Z)"
        ' |> filter(fn:(r) => r.deviceId == "sensor-1")'
    )


def test_get_formatted_flux_query_without_stop():
    bucket = "test_bucket"
    query_parameters = {
        "deviceId": "sensor-1",
        "start": "2020-01-02T03:44:00",
    }

    ret = get_formatted_flux_query(bucket, query_parameters)
    assert ret == (
        ' from(bucket:"test_bucket")'
        " |> range(start: 2020-01-02T03:44:00Z)"
        ' |> filter(fn:(r) => r.deviceId == "sensor-1")'
    )
