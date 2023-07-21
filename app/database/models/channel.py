from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.implementations.base_model import BaseModel
from app.database.models.meter import MeterModel


class ChannelModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    qanteon_name: Mapped[str] = mapped_column(nullable=True)
    qanteon_id: Mapped[int] = mapped_column(nullable=True, index=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey(MeterModel.id), index=True)
