import os

import pandas as pd

import aiohttp
import asyncio

from dotenv import load_dotenv

load_dotenv()


class Producer:
    """Producer class for the simulator."""

    def __init__(self):
        self.host = os.getenv("API_HOST")
        self.port = os.getenv("API_PORT")

    async def produce(self, payload: dict):
        endpoint = f"http://{self.host}:{self.port}/devices/events"

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload) as response:
                print("Status:", response.status)


async def simulate(start_date: str, end_date: str, status: str, device_id: str):
    """Retrieve status frequency.
    Args:
        start_date (str): initial date range.
        end_date: (str): end date range.
        status: (str): status.
        device_id: (str)device id.
    """
    timestamps = pd.date_range(start=start_date, end=end_date, freq="H")

    producer = Producer()
    for timestamp in timestamps:
        await producer.produce(
            {
                "deviceId": device_id,
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                "pressure": 212.0,
                "status": status,
                "temperature": 230,
            }
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(simulate("2020-01-03", "2020-01-05", "ON", "sensor-3"))
