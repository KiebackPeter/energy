from typing import Any, Dict, Generic, List, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as DTO
from sqlalchemy import insert, select, update
from asyncpg import UniqueViolationError
from sqlalchemy.exc import SQLAlchemyError

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

    def create(self, session:Session, new_obj: CreateDTO):
        return session.scalars(
            insert(self.model)
                .values(*new_obj)
                .returning(self.model)
        ).one()

    def get_by(self, session: Session, **kwargs):
        """Select exectly one or none with where clause"""
        return session.scalars(
            select(self.model).filter_by(**kwargs)
        ).one_or_none()

    def filter_by(self, session: Session, **kwargs):
        """Select all with where clause"""
        selection = session.scalars(
            select(self.model).filter_by(**kwargs)
        ).all()
        if not selection:
            HTTP_ERROR(404, "None found")
        return selection

    def update(self, session: Session,  id: int, **kwargs):
        """Update object with id"""
        try:
            obj = self.get_by(session, id = id)
            if not obj:
                return None
            for key, value in kwargs.items():
                setattr(obj, key, value)
            session.commit()
            return obj

        except SQLAlchemyError as e:
            session.rollback()
            return e
