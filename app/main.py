from http import HTTPStatus

from fastapi import FastAPI, Request

from .utils import get_environment_variables

app = FastAPI()


def create_app():
    """Application factory."""

    app = FastAPI()

    @app.middleware("http")
    async def add_credentials_middleware(request: Request, call_next):
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
    print(request.state.env_vars)
    return {}


@app.post("/devices/events", status_code=HTTPStatus.CREATED)
async def create_event():
    return {}


@app.get("/devices/histogram/{device_id}")
async def get_device_histogram():
    return {}
