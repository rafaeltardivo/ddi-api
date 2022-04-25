from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health():
    return {}


@app.post("/devices/events", status_code=HTTPStatus.CREATED)
async def create_event():
    return {}


@app.get("/devices/histogram/{device_id}")
async def device_histogram():
    return {}
