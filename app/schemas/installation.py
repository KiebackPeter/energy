from app.schemas.meter import MeterInBD, BaseModel


class InstallationPublic(BaseModel):
    name: str
    owner_email: str
    contracted_power_kw: int | None
    contracted_power_m3: int | None
    contracted_power_l: int | None


class InstallationProvider(InstallationPublic):
    provider_name: str
    provider_key: str

class InstallationCreateDTO(InstallationProvider):
    pass


class InstallationUpdateDTO(InstallationCreateDTO):
    name: str | None
    contracted_power_kw: int | None
    contracted_power_m3: int | None
    contracted_power_l: int | None


class InstallationInDB(InstallationCreateDTO):
    id: int
    meters: list[MeterInBD]
