from datetime import datetime
from pydantic import BaseModel


class MeterPublic(BaseModel):
    name: str
    commodity: str
    status: str


class MeterCreateDTO(MeterPublic):
    ean: str
    source_id: str
    installed_at: datetime


class MeterUpdateDTO(BaseModel):
    name: str | None
    status: str | None


class MeterUpdateQanteonIdDTO(BaseModel):
    qanteon_name: str | None
    qanteon_id: int


class MeterInBD(MeterCreateDTO):
    id: int
    installation_id: int
