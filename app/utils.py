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
