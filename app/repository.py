from influxdb_client import Point
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


async def add_event(credentials: dict, bucket: str, point: Point) -> bool:
    """Add event to bucket.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (dict): dict containing database credentials.
        point: (Point): influxdb data point.
    Returns:
        bool: True if the point was added, False otherwise.
    """
    async with InfluxDBClientAsync(**credentials) as client:
        write_api = client.write_api()
        result = await write_api.write(bucket=bucket, record=point)

    return result
