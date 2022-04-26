from http import HTTPStatus

from fastapi import FastAPI, Request, Query, Path

from .schemas import Event
from .utils import get_environment_variables, get_db_credentials, get_query_parameters
from .use_cases import create_event, get_histogram

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

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


@app.get("/health")
async def health(request: Request):
    db_credentials = get_db_credentials(request.state.env_vars)
    async with InfluxDBClientAsync(**db_credentials) as client:
        ready = await client.ping()

    return {"api": True, "db": ready}


@app.post("/devices/events", status_code=HTTPStatus.CREATED)
async def create_device_event(request: Request, event: Event):
    db_credentials = get_db_credentials(request.state.env_vars)
    bucket = request.state.env_vars["DOCKER_INFLUXDB_INIT_BUCKET"]
    result = await create_event(db_credentials, bucket, event)

    return {"success": result}


@app.get("/devices/histogram/{device_id}")
async def get_device_histogram(
    request: Request,
    device_id: str = Path(..., title="Device id", regex=r"^(sensor-[0-9]+)$"),
    start: str = Query(..., regex=r"^[1-9]\d{3}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"),
    stop: str | None = Query(None, regex=r"^[1-9]\d{3}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"),
):
    db_credentials = get_db_credentials(request.state.env_vars)
    bucket = request.state.env_vars["DOCKER_INFLUXDB_INIT_BUCKET"]
    query_parameters = get_query_parameters(device_id, start, stop)
    print(query_parameters)
    result = await get_histogram(db_credentials, bucket, query_parameters)

    return result
