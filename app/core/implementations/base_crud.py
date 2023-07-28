from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as DTO
from sqlalchemy import insert, select, update
from asyncpg import UniqueViolationError

# from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.core.logger import log  # create cutstom crud logger
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

    # async def do_create( # only use refrease
    #     self, session: Session, create_obj: CreateDTO
    # ) -> DatabaseModel:
    #     try:
    #         result = session.execute(
    #             insert(self.model).values(**create_obj).returning(self.model.id)
    #         )
    #         session.commit()
    #         return result.scalar_one()

    #     except UniqueViolationError as err:
    #         return err

    def get(self, session: Session, id: int):
        result = session.scalars(
            select(self.model)
            .filter_by(id = id)
        ).one_or_none()
        return result

    async def get_multi(
        self,
        session: Session,
        skip: int | None = 0,
        limit: int | None = 100,
    ):
        database_models = session.scalars(
            select(self.model).offset(skip).limit(limit)
        )
        if not database_models.all():
            HTTP_ERROR(404, "None found")

        return database_models.all()

    def update(
        self,
        session: Session,
        database_model: DatabaseModel | Dict[str, Any],
        update_obj: UpdateDTO | Dict[str, Any],
    ) -> DatabaseModel:

        if isinstance(database_model, dict):
            del database_model["_sa_instance_state"]
            database_model = self.model(**database_model)

        obj = jsonable_encoder(database_model)

        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict(exclude_unset=True)

        for field in obj:
            if field in update_data:
                setattr(database_model, field, update_data[field])

        session.scalar(
            update(self.model).values(database_model.__dict__)
        )
        return database_model
