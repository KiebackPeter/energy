from datetime import datetime, timedelta
from typing import Any, Optional, Union

from jose.jwt import decode, encode, JWTError

from app.core.error import HTTP_ERROR
from app.core.settings import env
from app.schemas.token import TokenPayload


def encode_access_token(subject: Union[str, Any], expires_delta: timedelta) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=env.API.tokenExpireMinutes)
    to_encode: dict[str, Any] = {"exp": expire, "sub": str(subject)}
    encoded_jwt = encode(to_encode, env.API.secretKey, algorithm="HS256")

    return encoded_jwt


def decode_access_token(token: str) -> TokenPayload | None:
    try:
        payload = decode(token, env.API.secretKey, algorithms="HS256")

        return TokenPayload(**payload)

    except JWTError as error:
        HTTP_ERROR(403, f"Invalid token: {error}")
