from .base_schema import BaseSchema
from .measurements import MeasurementCreateDTO


class ChannelPublic(BaseSchema):
    name: str


class ChannelCreateDTO(ChannelPublic):
    pass


class ChannelUpdateDTO(BaseSchema):
    qanteon_name: str | None
    qanteon_id: int | None
    latest_measurement: int | None


class ChannelInBD(ChannelPublic):
    id: int
    meter_id: int


class ChannelWithMeasurements(BaseSchema):
    channel_name: str
    measurements: list[MeasurementCreateDTO]
