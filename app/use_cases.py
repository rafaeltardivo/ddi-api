from collections import Counter

from .schemas import Event
from .repository import add_event, get_status_frequency
from .utils import get_formatted_flux_query


async def create_event(credentials: dict, bucket: str, event: Event) -> bool:
    """Create a new device event.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        event: (event): serialized Event object.
    Returns:
        bool: True if the event was successfully created, False otherwise.
    """
    data = {
        "measurement": "sensors",
        "tags": {"deviceId": event.device_id},
        "fields": {"status": event.status},
        "time": event.timestamp,
    }
    result = await add_event(credentials, bucket, data)

    return result


async def get_histogram(
    credentials: dict, bucket: str, query_parameters: dict
) -> tuple:
    """Get device histogram.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        query_parameters (dict): query parameters.
    Returns:
        dict: histogram (x=key, y=value).
    """
    query = get_formatted_flux_query(bucket, query_parameters)
    frequency = await get_status_frequency(credentials, query)

    histogram = Counter(frequency)
    return histogram
