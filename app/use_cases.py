from influxdb_client import Point

from .schemas import Event
from .repository import add_event


async def create_event(credentials: dict, bucket: str, event: Event) -> bool:
    """Create a new device event.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (dict): dict containing database credentials.
        event: (event): serialized Event object.
    Returns:
        bool: True if the event was successfully created, False otherwise.
    """
    point = (
        Point("sensors")
        .tag("deviceId", event.device_id)
        .field("status", event.status)
        .time(event.timestamp)
    )

    result = await add_event(credentials, bucket, point)
    return result
