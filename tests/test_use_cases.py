from collections import Counter

from unittest.mock import MagicMock, patch

import pytest

from app.use_cases import create_event, get_histogram
from app.schemas import Event
from app.utils import get_formatted_flux_query


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@pytest.mark.asyncio
@patch("app.use_cases.add_event", new_callable=AsyncMock)
async def test_create_event(mocked_add_event):
    mocked_add_event.return_value = True

    db_credentials = {"url": "mocked_url", "token": "mocked_token", "org": "mocked_org"}
    bucket = "test_bucket"
    event = Event(deviceId="sensor-1", status="ON", timestamp="2020-01-02T03:44:02")

    res = await create_event(db_credentials, bucket, event)

    mocked_add_event.assert_called_once_with(
        db_credentials,
        bucket,
        {
            "measurement": "sensors",
            "tags": {"deviceId": "sensor-1"},
            "fields": {"status": "ON"},
            "time": "2020-01-02T03:44:02",
        },
    )
    assert res is True


@pytest.mark.asyncio
@patch("app.use_cases.get_status_frequency", new_callable=AsyncMock)
async def test_get_histogram(mocked_get_status_frequency):
    mocked_frequency = ["ON", "ON", "OFF", "ACTIVE"]
    mocked_get_status_frequency.return_value = mocked_frequency

    db_credentials = {"url": "mocked_url", "token": "mocked_token", "org": "mocked_org"}
    bucket = "test_bucket"
    query_parameters = {
        "deviceId": "sensor-1",
        "start": "2020-01-02T03:44:02",
        "end": "2020-01-02T03:45:02",
    }

    res = await get_histogram(db_credentials, bucket, query_parameters)
    mocked_get_status_frequency.assert_called_once_with(
        db_credentials, get_formatted_flux_query(bucket, query_parameters)
    )
    assert res == Counter(mocked_frequency)
