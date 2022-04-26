import pytest

from http import HTTPStatus
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

from .fixtures import (
    device_id, start, stop, event_request_payload, histogram_response_payload
)
from .base import AsyncMock

client = TestClient(app)


@pytest.mark.asyncio
@patch("app.main.InfluxDBClientAsync.ping", new_callable=AsyncMock)
async def test_health(mocked_ping):
    mocked_ping.return_value = True

    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"api": True, "db": True}


@pytest.mark.asyncio
@patch("app.main.create_event", new_callable=AsyncMock)
async def test_create_event(mocked_create_event, event_request_payload):
    mocked_create_event.return_value = True

    response = client.post(
        "/devices/events",
        json=event_request_payload
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"success": True}


@pytest.mark.asyncio
@patch("app.main.get_histogram", new_callable=AsyncMock)
async def test_get_device_histogram(
        mocked_get_histogram, device_id, start, stop, histogram_response_payload
    ):
    mocked_get_histogram.return_value = histogram_response_payload

    qs = f"start={start}&stop={stop}"
    response = client.get(f"/devices/histogram/{device_id}?{qs}")
    assert response.json() == histogram_response_payload
