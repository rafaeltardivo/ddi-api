from collections import Counter

from .schemas import Event
from .repository import add_event, get_status_frequency, get_top_n_records


async def create_event(credentials: dict, bucket: str, event: Event) -> bool:
    """Create a new device event.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        event: (event): serialized Event object.
    Returns:
        bool: True if the event was successfully created, False otherwise.
    """
    result = await add_event(credentials, bucket, event.data())

    return result


async def get_histogram(
    credentials: dict, bucket: str, device_id: str, start: str, stop: str | None
) -> tuple:
    """Get device histogram.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        device_id (str): device id.
        start (str): initial interval timestamp.
        stop (str): final interval timestamp. Defaults to None.
    Returns:
        dict: histogram (x=key, y=value).
    """
    frequency = await get_status_frequency(credentials, bucket, device_id, start, stop)
    histogram = Counter(frequency)
    return histogram


async def get_indicator_top_n_records(
    credentials: dict, bucket: str, device_id: str, indicator: str, limit: int
) -> tuple:
    """Get indicator top n records.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        device_id (str): device id.
        indicator (str): device indicator.
        limit (int): limit for db query.
    Returns:
        list: top n ocurrences.
    """
    records = await get_top_n_records(credentials, bucket, device_id, indicator, limit)
    return records
