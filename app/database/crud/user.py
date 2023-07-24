from typing import Any, Dict, Union
from fastapi.encoders import jsonable_encoder

from passlib.context import CryptContext

from app.core.error import HTTP_ERROR
from app.core.implementations.base_crud import Session, CRUDBase # ,log
from app.database.models.user import UserModel
from app.schemas.user import UserCreateDTO, UserPublic, UserUpdateSelfDTO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class CRUDUser(CRUDBase[UserModel, UserCreateDTO, UserPublic]):
    def create(self, session: Session, create_obj: UserCreateDTO) -> UserModel:
        return self.commit(
            session,
            database_model=UserModel(
                full_name=create_obj.full_name,
                email=create_obj.email,
                hashed_password=get_password_hash(create_obj.password),
                is_superuser=False,
                installation_id=None,
            ),
        )

    def is_active(self, user: UserModel) -> bool:
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        return user.is_superuser

    def get_by_email(self, session: Session, email: str) -> UserModel | None:
        return session.query(UserModel).filter(UserModel.email == email).first()

    def authenticate(
        self, session: Session, email: str, password: str
    ) -> UserModel | None:
        user = self.get_by_email(session, email=email)
        if not user:
            HTTP_ERROR(400, "Incorrect email or password")

        elif not verify_password(password, user.hashed_password):
            HTTP_ERROR(400, "Incorrect email or password")

        return user

    def update_self(
        self,
        session: Session,
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
