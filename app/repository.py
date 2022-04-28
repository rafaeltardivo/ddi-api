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


async def get_status_frequency(
    credentials: dict, bucket: str, device_id: str, start: str, stop: str
) -> list:
    """Retrieve status frequency.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        device_id (str): device id.
        start (str): initial interval timestamp.
        stop (str): final interval timestamp. Defaults to None.
    Returns:
        list: occurrences of each status.
    """
    frequency = []

    query = f' from(bucket:"{bucket}")'
    if stop:
        query += f" |> range(start: {start}Z, stop: {stop}Z)"
    else:
        query += f" |> range(start: {start}Z)"
    query += f' |> filter(fn:(r) => r.deviceId == "{device_id}")'
    query += ' |> filter(fn:(r) => r._field == "status")'

    async with InfluxDBClientAsync(**credentials) as client:
        query_api = client.query_api()
        records = await query_api.query_stream(query)

        async for record in records:
            value = record.get_value()
            frequency.append(value)

    return frequency


async def get_top_n_records(
    credentials: dict, bucket: str, device_id: str, indicator: str, limit: int
) -> list:
    """Get top n records.
    Args:
        credentials (dict): dict containing database credentials.
        bucket (str): target bucket.
        device_id (str): device id.
        indicator (str): device indicator.
        limit (int): limit for query records..
    Returns:
        list: top n ocurrences.
    """
    results = []

    query = f' from(bucket:"{bucket}")'
    query += " |> range(start: 0)"
    query += f' |> filter(fn:(r) => r.deviceId == "{device_id}")'
    query += f' |> filter(fn:(r) => r._field == "{indicator}")'
    query += f" |> top(n: {limit})"

    async with InfluxDBClientAsync(**credentials) as client:
        query_api = client.query_api()
        records = await query_api.query_stream(query)

        async for record in records:
            value = record.get_value()
            results.append(value)

    return results
