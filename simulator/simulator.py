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
                if response.status != 201:
                    print("failed to create event!")


async def simulate(start_date: str, end_date: str):
    """Retrieve status frequency.
    Args:
        start_date (str): initial date range.
        end_date: (str): end date range.
    """
    timestamps = pd.date_range(start=start_date, end=end_date, freq="min")

    producer = Producer()

    for timestamp in timestamps:
        await producer.produce(
            {
                "deviceId": f"sensor-{random.randint(1, 10)}",
                "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S"),
                "pressure": round(random.uniform(0, 200), 1),
                "status": random.choice(["ON", "OFF", "ACTIVE", "INACTIVE"]),
                "temperature": round(random.uniform(0, 250), 1),
            }
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        simulate(
            "2020-01-01",
            "2020-01-02",
        )
    )
