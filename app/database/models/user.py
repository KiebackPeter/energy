"""User table"""
from .base_model import (
    datetime,
    ForeignKey,
    BaseModel,
    Mapped,
    mapped_column
)


class UserModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.today())
    installation_id: Mapped[int | None] = mapped_column(ForeignKey("installation.id"))
