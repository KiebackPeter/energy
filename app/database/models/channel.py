from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.implementations.base_model import BaseModel


class ChannelModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    qanteon_name: Mapped[str] = mapped_column(nullable=True)
    qanteon_id: Mapped[int] = mapped_column(nullable=True, index=True)
    latest_measurement: Mapped[float] = mapped_column()
    meter_id: Mapped[int] = mapped_column(ForeignKey("meter.id"), index=True)
