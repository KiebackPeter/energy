from typing import Any, Dict, Union
from fastapi.encoders import jsonable_encoder

from passlib.context import CryptContext
from sqlalchemy import select

from app.core.error import HTTP_ERROR
from app.database.models.user import UserModel
from app.schemas.user import UserCreateDTO, UserPublic, UserUpdateSelfDTO
from app.core.implementations.base_crud import AsyncSession, CRUDBase # ,log

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class CRUDUser(CRUDBase[UserModel, UserCreateDTO, UserPublic]):
    async def create(self, session: AsyncSession, create_obj: UserCreateDTO):
        user_data = jsonable_encoder(create_obj)
        user_data["hashed_password"] = get_password_hash(create_obj.password)
        user_data["is_superuser"] = False
        user_data["installation_id"] = None

        return await self.do_create(session,user_data)

    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser

    async def get_credentials(self, session: AsyncSession, email: str):
        return await session.scalar(
        select(self.model).filter(self.model.email == email)
        )

    async def authenticate(
        self, session: AsyncSession, email: str, password: str
    ):
        user = await self.get_credentials(session, email=email)
        if user is None:
            HTTP_ERROR(400, "Incorrect email")

        elif not verify_password(password, user.hashed_password):
            HTTP_ERROR(400, "Incorrect email and password")

        return user

    def update_self(
        self,
        session: AsyncSession,
        model: UserModel,
        update_obj: Union[UserUpdateSelfDTO, Dict[str, Any]],
    ):
        update_data = jsonable_encoder(update_obj)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password

        updated_user = self.update(session, database_model=model, update_obj=update_data)

        return updated_user


user_crud = CRUDUser(UserModel)
