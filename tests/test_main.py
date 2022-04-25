from http import HTTPStatus
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {}


def test_create_event():
    response = client.post("/devices/events")
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {}


def test_get_device_histogram():
    sensor_id = "sensor-1"

    response = client.get(f"/devices/histogram/{sensor_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {}
