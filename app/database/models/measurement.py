"""Measurement table"""
from .base_model import (
    PrimaryKeyConstraint,
    UniqueConstraint,
    ForeignKey,
    BaseModel,
    Mapped,
    mapped_column,
)


class MeasurementModel(BaseModel):
    __table_args__ = (
        UniqueConstraint(
            "timestamp", "channel_id", name="timestamp_on_channel_id_contstraint"
        ),
        PrimaryKeyConstraint("timestamp", "channel_id"),
        {},
    )
    timestamp: Mapped[float] = mapped_column(index=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channel.id"), index=True)
    value: Mapped[float] = mapped_column()
    accumulated: Mapped[float | None] = mapped_column()
