import pytest

from http import HTTPStatus
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app

from .fixtures import device_id, start, stop

client = TestClient(app)


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@pytest.mark.asyncio
@patch("app.main.InfluxDBClientAsync.ping", new_callable=AsyncMock)
async def test_health(mocked_ping):
    mocked_ping.return_value = True

    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"api": True, "db": True}


@pytest.mark.asyncio
@patch("app.main.create_event", new_callable=AsyncMock)
async def test_create_event(mocked_create_event):
    mocked_create_event.return_value = True

    response = client.post(
        "/devices/events",
        json={
            "deviceId": "sensor-1",
            "timestamp": "2020-01-02T03:44:02",
            "pressure": 212.0,
            "status": "ON",
            "temperature": 230,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"success": True}


@pytest.mark.asyncio
@patch("app.main.get_histogram", new_callable=AsyncMock)
async def test_get_device_histogram(mocked_get_histogram, device_id, start, stop):
    mocked_response = {
        "ON": 1,
        "OFF": 2,
        "ACTIVE": 5,
        "INACTIVE": 0,
    }
    mocked_get_histogram.return_value = mocked_response

    qs = f"start={start}&stop={stop}"
    response = client.get(f"/devices/histogram/{device_id}?{qs}")
    assert response.json() == mocked_response
