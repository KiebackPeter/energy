from pydantic import BaseModel

from app.schemas.measurements import MeasurementCreateDTO


class ChannelPublic(BaseModel):
    name: str


class ChannelCreateDTO(ChannelPublic):
    pass


class ChannelUpdateDTO(BaseModel):
    qanteon_name: str | None
    qanteon_id: int | None
    latest_measurement: int | None


class ChannelInBD(ChannelPublic):
    id: int
    meter_id: int

class ChannelWithMeasurements(BaseModel):
    channel_name: str
    measurements: list[MeasurementCreateDTO]