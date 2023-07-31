"""A base class for database table, with common imports"""

from datetime import datetime
from sqlalchemy import (
    PrimaryKeyConstraint,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(index=True)
    __name__: str

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()[:-5]
