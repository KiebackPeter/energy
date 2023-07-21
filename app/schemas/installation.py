from pydantic import BaseModel

from app.schemas.meter import MeterInBD


class InstallationPublic(BaseModel):
    name: str
    owner_email: str
    provider_name: str | None
    contracted_power_kw: int | None
    contracted_power_m3: int | None
    contracted_power_l: int | None


class InstallationCreateDTO(BaseModel):
    name: str
    provider_name: str | None
    provider_key: str | None


class InstallationUpdateDTO(InstallationCreateDTO):
    name: str | None
    contractor_email: str | None
    contracted_power_kw: int | None
    contracted_power_m3: int | None
    contracted_power_l: int | None


class InstallationInDB(InstallationCreateDTO):
    id: int
    meters: list[MeterInBD]
