from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.implementations.base_model import BaseModel
from app.database.models.meter import MeterModel


class InstallationModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    owner_email: Mapped[str] = mapped_column(index=True)
    contracted_power_kw: Mapped[int | None] = mapped_column()
    contracted_power_m3: Mapped[int | None] = mapped_column()
    contracted_power_l: Mapped[int | None] = mapped_column()
    provider_name: Mapped[str | None] = mapped_column()
    provider_key: Mapped[str | None] = mapped_column()
    meters: Mapped[list[MeterModel]] = relationship(backref="installation")
