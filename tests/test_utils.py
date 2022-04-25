import os
import pytest
from unittest import mock

from app.exceptions import MissingEnvironmentVariableError
from app.utils import (
    load_environment_variable,
    get_environment_variables,
    get_db_credentials,
)


def test_load_environment_variable():
    key, value = "FOO", "BAR"

    with mock.patch.dict(os.environ, {key: value}):
        var = load_environment_variable(key)
        assert var == value


def test_load_missing_environment_variable():
    with pytest.raises(MissingEnvironmentVariableError):
        load_environment_variable("MISSING")


def test_get_environment_variables():
    env_vars = {"ONE": "1", "TWO": "2"}
    with mock.patch.dict(os.environ, env_vars):
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
