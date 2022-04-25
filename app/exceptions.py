class MissingEnvironmentVariableError(Exception):
    """Exception raised for missing environment variable.

    Attributes:
        var (str): missing environment variable.
    """

    def __init__(self, var):
        self.var = var
        super().__init__(self.var)

    def __str__(self):
        return f"Missing environment variable: {self.var}"
