import random
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
        print(payload)
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload) as response:
                if response.status == 201:
                    return payload["status"]


async def simulate(start_date: str, end_date: str, status: str, device_ids: list):
    """Retrieve status frequency.
    Args:
        start_date (str): initial date range.
        end_date: (str): end date range.
        status: (str): status.
        device_id: (str)device id.
    """
    statuses = ["ON", "OFF", "ACTIVE", "INACTIVE"]
    timestamps = pd.date_range(start=start_date, end=end_date, freq="min")

    producer = Producer()

    for device_id in device_ids:
        production_track = {}

        for timestamp in timestamps:
            ret = await producer.produce(
                {
                    "deviceId": device_id,
                    "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                    "pressure": 212.0,
                    "status": random.choice(statuses) if status == "random" else status,
                    "temperature": 230,
                }
            )

            try:
                production_track[ret] += 1
            except KeyError:
                production_track[ret] = 1

        print(f"Production track for device {device_id}:", production_track)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        simulate(
            "2020-01-01",
            "2020-01-02",
            "random",
            ["sensor-1", "sensor-2", "sensor-3", "sensor-5", "sensor-6", "sensor-7"],
        )
    )
