from datetime import datetime
from .base_schema import BaseSchema


class MeterPublic(BaseSchema):
    name: str
    commodity: str
    status: str


class MeterCreateDTO(MeterPublic):
    ean: str
    source_id: str
    installed_at: datetime


class MeterUpdateDTO(BaseSchema):
    name: str | None
    status: str | None


class MeterUpdateQanteonIdDTO(BaseSchema):
    qanteon_name: str | None
    qanteon_id: int


class MeterInBD(MeterCreateDTO):
    id: int
    installation_id: int
