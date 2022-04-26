from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


async def get_health(credentials: dict) -> tuple:
    """Service healthcheck.
    Args:
        credentials (dict): dict containing database credentials.
    Returns:
        tuple: tuple containing api and db statuses.
    """
    async with InfluxDBClientAsync(**credentials) as client:
        ready = await client.ping()

    return True, ready
