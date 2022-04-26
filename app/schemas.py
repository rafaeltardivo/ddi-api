from pydantic import BaseModel, Field

from enum import Enum


class StatusEnum(str, Enum):
    """Enum for event statuses."""

    on = "ON"
    off = "OFF"
    active = "ACTIVE"
    inactive = "INACTIVE"


class Event(BaseModel):
    """Device event base model."""

    device_id: str = Field(alias="deviceId")
    status: StatusEnum
    timestamp: str

    def data(self):
        """Return influxdb record compatible dict."""
        return {
            "measurement": "sensors",
            "tags": {"deviceId": self.device_id},
            "fields": {"status": self.status},
            "time": self.timestamp,
        }

    class Config:
        use_enum_values = True
