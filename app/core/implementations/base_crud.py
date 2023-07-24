from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as DTO
from sqlalchemy.orm import Session #

from app.core.logger import log # create cutstom crud logger
from app.core.error import HTTP_ERROR
from app.core.implementations.base_model import BaseModel

DatabaseModel = TypeVar("DatabaseModel", bound=BaseModel)
CreateDTO = TypeVar("CreateDTO", bound=DTO)
UpdateDTO = TypeVar("UpdateDTO", bound=DTO)


class CRUDBase(Generic[DatabaseModel, CreateDTO, UpdateDTO]):
    def __init__(self, model: Type[DatabaseModel]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def commit(self, session: Session, database_model: DatabaseModel) -> DatabaseModel:
        session.add(database_model)
        session.commit()
        session.refresh(database_model)
        return database_model

    def create(self, session: Session, create_obj: CreateDTO) -> DatabaseModel:
        create_obj_data = jsonable_encoder(create_obj)
        database_model = self.model(**create_obj_data)

        return self.commit(session, database_model)

    def get(self, session: Session, id: int) -> DatabaseModel:
        database_model: DatabaseModel | None = (
            session.query(self.model).filter(self.model.id == id).first()
        )
        if not database_model:
            return HTTP_ERROR(404, "Not found")
        return database_model

    def get_multi(
        self, session: Session, skip: int | None = 0, limit: int | None = 100
    ) -> List[DatabaseModel]:
        database_models: list[DatabaseModel] | None = (
            session.query(self.model).offset(skip).limit(limit).all()
        )
        if not database_models:
            HTTP_ERROR(404, "None found")

        return database_models

    def update(
        self,
        session: Session,
        database_model: DatabaseModel,
        update_obj: Union[UpdateDTO, Dict[str, Any]]
    ) -> DatabaseModel:
        obj = jsonable_encoder(database_model)

        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict(exclude_unset=True)

        for field in obj:
            if field in update_data:
                setattr(database_model, field, update_data[field])

        return self.commit(session, database_model)
