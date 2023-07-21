from pydantic import BaseModel


class MeasurementPublic(BaseModel):
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
