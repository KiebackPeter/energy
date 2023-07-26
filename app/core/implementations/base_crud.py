from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as DTO
from sqlalchemy import insert, select
from asyncpg import UniqueViolationError

# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction
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

    async def do_create(
        self, session: AsyncSession, create_obj: CreateDTO
    ) -> DatabaseModel:
        try:
            return await session.scalar(
                insert(self.model).values(**create_obj).return_defaults()
            )
        except UniqueViolationError as err:
            return err

    async def get(self, session: AsyncSession, id: int):
        result = await session.scalar(
            select(self.model).filter(self.model.id == id).limit(1)
        )
        await session.refresh(result)
        return result

    async def get_multi(
        self,
        session: AsyncSession,
        skip: int | None = 0,
        limit: int | None = 100,
    ):
        database_models = await session.scalars(
            select(self.model).offset(skip).limit(limit)
        )
        if not database_models.all():
            HTTP_ERROR(404, "None found")

        return database_models.all()

    def update(
        self,
        session: AsyncSessionTransaction,
        database_model: DatabaseModel,
        update_obj: Union[UpdateDTO, Dict[str, Any]],
    ) -> DatabaseModel:
        obj = jsonable_encoder(database_model)

        if isinstance(update_obj, dict):
            update_data = update_obj
        else:
            update_data = update_obj.dict(exclude_unset=True)

        for field in obj:
            if field in update_data:
                setattr(database_model, field, update_data[field])

        return self.refresh(session, database_model)
