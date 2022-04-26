from unittest.mock import MagicMock, patch

import pytest

from app.use_cases import create_event
from app.schemas import Event


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

    mocked_add_event.assert_called_once()
    assert res is True
