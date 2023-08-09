from sqlalchemy.orm import DeclarativeBase, declared_attr, class_mapper
# from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(DeclarativeBase):
    id: int
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()[:-5]
    
    def primary_keys(self):
        columns = [c.key for c in class_mapper(self.__class__).columns if c.primary_key]
        return {c: getattr(self, c) for c in columns}
            
    def to_dict(self):
        columns = [c.key for c in class_mapper(self.__class__).columns if not c.primary_key]
        return {c: getattr(self, c) for c in columns}
        