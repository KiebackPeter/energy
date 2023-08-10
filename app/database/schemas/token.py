from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: int


class TokenData(BaseModel):
    email: EmailStr | None = None
    scopes: list[str] = []
