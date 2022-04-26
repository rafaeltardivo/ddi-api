from unittest.mock import MagicMock, patch

import pytest

from app.use_cases import get_health


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)


@pytest.mark.asyncio
@patch("app.use_cases.InfluxDBClientAsync.ping", new_callable=AsyncMock)
async def test_get_health(mocked_ping):
    mocked_ping.return_value = True
    db_credentials = {"url": "mocked_url", "token": "mocked_token", "org": "mocked_org"}
    res = await get_health(db_credentials)

    mocked_ping.assert_called_once()
    assert res == (True, True)
