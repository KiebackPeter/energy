from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.implementations.base_model import BaseModel


class MeterModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    commodity: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column()
    ean: Mapped[str] = mapped_column(unique=True)
    source_id: Mapped[str] = mapped_column()
    installed_at: Mapped[datetime] = mapped_column()
    installation_id: Mapped[int] = mapped_column(
        ForeignKey("installation.id"), index=True
    )
