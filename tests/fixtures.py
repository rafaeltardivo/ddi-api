import pytest

from app.schemas import Event


@pytest.fixture
def db_credentials():
    return {"url": "http://mocked.url", "token": "mocked_token", "org": "mocked_org"}


@pytest.fixture
def bucket():
    return "mocked_bucket"


@pytest.fixture
def event():
    return Event(deviceId="sensor-1", status="ON", timestamp="2020-01-02T03:44:02")


@pytest.fixture
def query_parameters():
    return {
        "deviceId": "sensor-1",
        "start": "2020-01-02T03:44:02",
        "end": "2020-01-02T03:45:02",
    }


@pytest.fixture
def frequency():
    return ["ON", "ON", "OFF", "ACTIVE"]
