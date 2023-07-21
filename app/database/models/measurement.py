from sqlalchemy import PrimaryKeyConstraint, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.implementations.base_model import BaseModel
from app.database.models.channel import ChannelModel


class MeasurementModel(BaseModel):
    __table_args__ = (
        UniqueConstraint(
            "timestamp", "channel_id", name="timestamp_on_channel_id_contstraint"
        ),
        PrimaryKeyConstraint("timestamp", "channel_id"),
        {},
    )
    timestamp: Mapped[float] = mapped_column(index=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey(ChannelModel.id), index=True)
    value: Mapped[float] = mapped_column()
    accumulated: Mapped[float | None] = mapped_column()
