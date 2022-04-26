from collections import Counter

from unittest.mock import patch

import pytest

from app.use_cases import create_event, get_histogram
from app.utils import get_formatted_flux_query
from .fixtures import db_credentials, bucket, event, query_parameters, frequency
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
    mocked_get_status_frequency, db_credentials, bucket, query_parameters, frequency
):
    mocked_get_status_frequency.return_value = frequency

    res = await get_histogram(db_credentials, bucket, query_parameters)
    mocked_get_status_frequency.assert_called_once_with(
        db_credentials, get_formatted_flux_query(bucket, query_parameters)
    )
    assert res == Counter(frequency)
