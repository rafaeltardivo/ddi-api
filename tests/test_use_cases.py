from collections import Counter

from unittest.mock import patch

import pytest

from app.use_cases import create_event, get_histogram
from .fixtures import (
    db_credentials, bucket,
    device_id,
    start,
    stop,
    event,
    frequency
)
from .base import AsyncMock


@pytest.mark.asyncio
@patch("app.use_cases.add_event", new_callable=AsyncMock)
async def test_create_event(mocked_add_event, db_credentials, bucket, event):
    mocked_add_event.return_value = True

    res = await create_event(db_credentials, bucket, event)
    mocked_add_event.assert_called_once_with(db_credentials, bucket, event.data())
    assert res is True


@pytest.mark.asyncio
@patch("app.use_cases.get_status_frequency", new_callable=AsyncMock)
async def test_get_histogram(
    mocked_get_status_frequency,
    frequency, db_credentials,
    bucket,
    device_id,
    start,
    stop
):
    mocked_get_status_frequency.return_value = frequency

    res = await get_histogram(db_credentials, bucket, device_id, start, stop)
    mocked_get_status_frequency.assert_called_once_with(
        db_credentials, bucket, device_id, start, stop
    )
    assert res == Counter(frequency)
