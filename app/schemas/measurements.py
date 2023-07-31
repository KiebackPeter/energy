from .base_schema import BaseSchema


class MeasurementPublic(BaseSchema):
    value: float
    timestamp: float
    accumulated: int


# Properties for creating
class MeasurementCreateDTO(MeasurementPublic):
    accumulated: int | None = None


# Properties for updates
class MeasurementUpdateDTO(MeasurementPublic):
    pass


class MeasurementInDB(MeasurementPublic):
    channel_id: int
