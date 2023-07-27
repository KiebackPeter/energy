
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(AsyncAttrs, DeclarativeBase):
    id: int
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()[:-5]
