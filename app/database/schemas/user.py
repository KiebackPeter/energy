from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    full_name: str
    email: EmailStr


class UserCreateDTO(UserPublic):
    password: str


class UserUpdateSelfDTO(BaseModel):
    password: str | None = None
    full_name: str | None = None
    email: EmailStr | None = None


class User(UserPublic):
    is_active: bool
    is_superuser: bool
    installation_id: int | None


class UserinDB(User):
    id: int
    hashed_password: str
