from http import HTTPStatus

from fastapi import FastAPI, Request

from .utils import get_environment_variables, get_db_credentials

app = FastAPI()


def create_app():
    """Application factory."""

    app = FastAPI()

    @app.middleware("http")
    async def env_vars_middleware(request: Request, call_next):
        """Middleware for state persistence of env vars."""
        request.state.env_vars = get_environment_variables(
            [
                "INFLUXDB_HOST",
                "INFLUXDB_PORT",
                "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN",
                "DOCKER_INFLUXDB_INIT_ORG",
                "DOCKER_INFLUXDB_INIT_BUCKET",
            ]
        )
        response = await call_next(request)
        return response

    return app


app = create_app()


@app.get("/health")
async def health(request: Request):
    db_credentials = get_db_credentials(request.state.env_vars)
    return {}


@app.post("/devices/events", status_code=HTTPStatus.CREATED)
async def create_event():
    db_credentials = get_db_credentials(request.state.env_vars)
    return {}


@app.get("/devices/histogram/{device_id}")
async def get_device_histogram():
    db_credentials = get_db_credentials(request.state.env_vars)
    return {}
