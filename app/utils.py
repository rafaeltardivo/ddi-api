import os

from dotenv import load_dotenv
from .exceptions import MissingEnvironmentVariableError

load_dotenv()


def load_environment_variable(variable: str) -> str:
    """Loads environment variable into memory.

    Args:
        variable (str): environment variable to be loaded.
    Raises:
        MissingEnvironmentVariableError: if the variable is missing.
    """
    value = os.getenv(variable)

    if value is None:
        raise MissingEnvironmentVariableError(variable)

    return value


def get_environment_variables(variables: list) -> dict:
    """Retrieves environment variables.
    Args:
        variables (list): variable names.
    Returns:
        dict: dictionary containing all requested environment variables.
    Raises:
        MissingEnvironmentVariableError: if one of the variables is missing.
    """
    return {var: load_environment_variable(var) for var in variables}


def get_db_credentials(env_vars: dict) -> dict:
    """Retrieves database credentials.
    Args:
        env_vars (dict): loaded env vars.
    Returns:
        dict: dictionary containing all formatted database credentials.
    """
    return {
        "url": f"http://{env_vars['INFLUXDB_HOST']}:{env_vars['INFLUXDB_PORT']}",
        "token": env_vars["DOCKER_INFLUXDB_INIT_ADMIN_TOKEN"],
        "org": env_vars["DOCKER_INFLUXDB_INIT_ORG"],
    }
