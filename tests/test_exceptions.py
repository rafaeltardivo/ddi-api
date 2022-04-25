from app.exceptions import MissingEnvironmentVariableError


def test_missing_environment_variable_error():
    missing_env_var = "foo"

    e = MissingEnvironmentVariableError(missing_env_var)
    assert str(e) == f"Missing environment variable: {missing_env_var}"
