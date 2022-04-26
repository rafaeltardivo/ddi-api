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
def start():
    return "2020-01-02T03:44:00"


@pytest.fixture
def stop():
    return "2020-01-02T03:48:00"


@pytest.fixture
def device_id():
    return "sensor-1"


@pytest.fixture
def query_parameters():
    return {
        "deviceId": "sensor-1",
        "start": "2020-01-02T03:44:00",
        "stop": "2020-01-02T03:48:00",
    }


@pytest.fixture
def qs(start, stop):
    return f"start={start}&stop={stop}"


@pytest.fixture
def frequency():
    return ["ON", "ON", "OFF", "ACTIVE"]


@pytest.fixture
def env_vars():
    return {
        "INFLUXDB_HOST": "mocked_influxdb",
        "INFLUXDB_PORT": "8086",
        "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN": "mocked_token",
        "DOCKER_INFLUXDB_INIT_ORG": "mocked_org",
    }
