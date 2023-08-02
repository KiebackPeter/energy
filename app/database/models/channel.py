"""Channel table"""
from .measurement import MeasurementModel
from .base_model import (
    ForeignKey,
    BaseModel,
    Mapped,
    mapped_column,
    relationship,
)


class ChannelModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    qanteon_name: Mapped[str] = mapped_column(nullable=True)
    qanteon_id: Mapped[int] = mapped_column(nullable=True, index=True)
    latest_measurement: Mapped[float] = mapped_column(nullable=True)
    meter_id: Mapped[int] = mapped_column(ForeignKey("meter.id"), index=True)
    measurements: Mapped[list[MeasurementModel]] = relationship(
        "MeasurementModel",
        backref="channel",
        cascade="all, delete-orphan",
    )
