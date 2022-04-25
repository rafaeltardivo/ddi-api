import os
import pytest
from unittest import mock

from app.exceptions import MissingEnvironmentVariableError
from app.utils import load_environment_variable


@mock.patch.dict(os.environ, {"FOO": "BAR"})
def test_load_environment_variable():
    var = load_environment_variable("FOO")
    assert var == "BAR"


def test_load_missing_environment_variable():

    with pytest.raises(MissingEnvironmentVariableError):
        load_environment_variable("MISSING")
