from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


async def add_event(credentials: dict, bucket: str, data: dict) -> bool:
    """Add event to bucket.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (dict): dict containing database credentials.
        data: (dict): data to be added to INfluxDB.
    Returns:
        bool: True if the point was added, False otherwise.
    """
    async with InfluxDBClientAsync(**credentials) as client:
        write_api = client.write_api()
        result = await write_api.write(bucket=bucket, record=data)

    return result


async def get_status_frequency(credentials: dict, query: str) -> list:
    """Retrieve status frequency.
    Args:
        credentials (dict): dict containing database credentials.
        query: (str): flux formatted query.
    Returns:
        list: occurrences of each status.
    """
    frequency = []

    async with InfluxDBClientAsync(**credentials) as client:
        query_api = client.query_api()
        records = await query_api.query_stream(query)

        async for record in records:
            value = record.get_value()
            frequency.append(value)

    return frequency
