from app.database.schemas.meter import MeterInBD, BaseModel


class InstallationPublic(BaseModel):
    name: str
    owner_email: str | None = None
    contracted_power_kw: int | None = None
    contracted_power_m3: int | None = None
    contracted_power_l: int | None = None


class InstallationProvider(InstallationPublic):
    provider_name: str
    provider_key: str

class InstallationCreateDTO(InstallationProvider):
    pass


class InstallationUpdateDTO(BaseModel):
    name: str | None = None
    contracted_power_kw: int | None = None
    contracted_power_m3: int | None = None
    contracted_power_l: int | None = None


class InstallationInDB(InstallationCreateDTO):
    id: int
    meters: list[MeterInBD]
