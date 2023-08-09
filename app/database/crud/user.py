from typing import Any, Dict, Union
from fastapi.encoders import jsonable_encoder

from passlib.context import CryptContext
from sqlalchemy import select, insert

from app.core.error import HTTP_ERROR
from app.database.models.user import UserModel
from app.schemas.user import UserCreateDTO, UserPublic, UserUpdateSelfDTO
from app.database.crud.base_crud import Session, CRUDBase  # ,log

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class CRUDUser(CRUDBase[UserModel, UserCreateDTO, UserPublic]):
    def create(self, session: Session, create_obj: UserCreateDTO):
        user_data = jsonable_encoder(create_obj)
        del user_data["password"]
        user_data["hashed_password"] = get_password_hash(create_obj.password)

        return session.scalar(
            insert(self.model).values(user_data).returning(self.model)
        )

    def get_credentials(self, session: Session, email: str):
        return session.scalars(
            select(self.model).where(self.model.email == email)
        ).first()

    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser

    def authenticate(self, session: Session, email: str, password: str):
        user = self.get_credentials(session, email=email)

        if user is None:
            HTTP_ERROR(400, "Incorrect email")

        elif not verify_password(password, user.hashed_password):
            HTTP_ERROR(400, "Incorrect email and password")

        return user

    def update_self(
        self,
        session: Session,
        model: UserModel,
        update_obj: Dict[str, Any],
    ) -> UserModel:
        if "password" in update_obj.keys():
            hashed_password = get_password_hash(update_obj["password"])
            del update_obj["password"]
            update_obj["hashed_password"] = hashed_password

        updated_user = self.put(session, database_model=model, update_obj=update_obj)

        return updated_user


user_crud = CRUDUser(UserModel)
