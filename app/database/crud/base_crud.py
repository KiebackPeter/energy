from typing import Any, Dict, Generic, Sequence, Type, TypeVar
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel as DTO
from sqlalchemy import insert, select, update, desc
from sqlalchemy.exc import SQLAlchemyError

# from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from app.core.logger import log  # create cutstom crud logger
from app.core.error import HTTP_ERROR
from app.database.models.base_model import BaseModel

DatabaseModel = TypeVar("DatabaseModel", bound=BaseModel)
CreateDTO = TypeVar("CreateDTO", bound=DTO)
UpdateDTO = TypeVar("UpdateDTO", bound=DTO)


class CRUDBase(Generic[DatabaseModel, CreateDTO, UpdateDTO]):
    def __init__(self, model: Type[DatabaseModel]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""
        self.model = model

    def create(self, session: Session, create_obj: CreateDTO) -> DatabaseModel:
        """Add object to database and return with all values"""
        return session.scalars(
            insert(self.model).values(*create_obj).returning(self.model)
        ).one()

    def get_by(self, session: Session, **kwargs) -> DatabaseModel | None:
        """Select exectly one or none with where clause"""
        return session.scalars(select(self.model).filter_by(**kwargs)).one_or_none()

    def filter_by(self, session: Session, **kwargs) -> Sequence[DatabaseModel] | list:
        """Select all with where clause"""
        selection = session.scalars(select(self.model).filter_by(**kwargs)).all()
        if not selection:
            HTTP_ERROR(404, "None found")
        return selection


    def update(
        self,
        session: Session,
        database_model: DatabaseModel | Dict[str, Any],
        update_obj: Dict[str, Any],
    ) -> DatabaseModel:

        if isinstance(database_model, dict):
            del database_model["_sa_instance_state"]
            database_model = self.model(**database_model)

        obj = jsonable_encoder(database_model, exclude_defaults=True)

        for field in obj:
            if field in update_obj.keys():
                setattr(database_model, field, update_obj[field])

        session.scalar(
            update(self.model).values(database_model)
        )
        return database_model
    
    # def update(
    #     self, session: Session, id: int, **kwargs
    # ) -> DatabaseModel | KeyError | SQLAlchemyError:
    #     """Update object with id"""
    #     try:
    #         obj = self.get_by(session, id=id)
    #         if not obj:
    #             raise KeyError

    #         for key, value in kwargs.items():
    #             print(f"SETTING: {key}: {value}")
    #             setattr(obj, key, value)
    #         print("SETTING:",  obj.__dict__)
    #         updated_obj = session.scalar(
    #             update(self.model)
    #             .where(self.model.id == id)
    #             .values(**obj)
    #         )
    #         session.commit()
    #         session.refresh(updated_obj)
    #         return obj

    #     except (SQLAlchemyError, KeyError) as err:
    #         session.rollback()
    #         return err
