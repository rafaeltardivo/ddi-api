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

from .fixtures import env_vars, query_parameters, bucket, device_id, start, stop


def test_load_environment_variable():
    key, value = "FOO", "BAR"

    with patch.dict(os.environ, {key: value}):
        var = load_environment_variable(key)

        assert var == value


def test_load_missing_environment_variable():
    with pytest.raises(MissingEnvironmentVariableError):
        load_environment_variable("MISSING")


def test_get_environment_variables(env_vars):
    with patch.dict(os.environ, env_vars):
        ret = get_environment_variables(env_vars.keys())

        assert ret == env_vars


def test_get_db_credentials(env_vars):
    ret = get_db_credentials(env_vars)

    assert ret["org"] == env_vars["DOCKER_INFLUXDB_INIT_ORG"]
    assert ret["token"] == env_vars["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"]
    assert (
        ret["url"] == f"http://{env_vars['INFLUXDB_HOST']}:{env_vars['INFLUXDB_PORT']}"
    )


def test_get_query_parameters(device_id, start, stop):
    ret = get_query_parameters(device_id, start, stop)

    assert ret["deviceId"] == device_id
    assert ret["start"] == start
    assert ret["stop"] == stop


def test_get_formatted_flux_query(bucket, query_parameters):
    ret = get_formatted_flux_query(bucket, query_parameters)

    assert ret == (
        f' from(bucket:"{bucket}")'
        f' |> range(start: {query_parameters["start"]}Z, stop: {query_parameters["stop"]}Z)'
        f' |> filter(fn:(r) => r.deviceId == "{query_parameters["deviceId"]}")'
    )


def test_get_formatted_flux_query_without_stop(bucket, query_parameters):
    query_parameters.pop("stop")
    ret = get_formatted_flux_query(bucket, query_parameters)

    assert ret == (
        f' from(bucket:"{bucket}")'
        f' |> range(start: {query_parameters["start"]}Z)'
        f' |> filter(fn:(r) => r.deviceId == "{query_parameters["deviceId"]}")'
    )
