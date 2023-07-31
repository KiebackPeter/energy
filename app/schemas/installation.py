from .base_schema import BaseSchema
from .meter import MeterInBD


class InstallationPublic(BaseSchema):
    name: str
    owner_email: str
    contracted_power_kw: int | None = None
    contracted_power_m3: int | None = None
    contracted_power_l: int | None = None


class InstallationProvider(InstallationPublic):
    provider_name: str
    provider_key: str


class InstallationCreateDTO(InstallationProvider):
    pass


class InstallationUpdateDTO(BaseSchema):
    name: str | None = None
    contracted_power_kw: int | None
    contracted_power_m3: int | None
    contracted_power_l: int | None


class InstallationInDB(InstallationCreateDTO):
    id: int
    meters: list[MeterInBD]
