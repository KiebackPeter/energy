from .base_schema import BaseSchema


class UserPublic(BaseSchema):
    full_name: str
    email: str


class UserCreateDTO(UserPublic):
    password: str


class UserUpdateSelfDTO(BaseSchema):
    password: str | None = None
    full_name: str | None = None
    email: str | None = None


class User(UserPublic):
    is_active: bool
    is_superuser: bool
    installation_id: int | None


class UserinDB(User):
    id: int
    hashed_password: str
