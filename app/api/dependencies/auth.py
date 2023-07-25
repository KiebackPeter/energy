
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.api.dependencies.token import decode_access_token, encode_access_token, timedelta
from app.core.error import HTTP_ERROR
from app.core.settings import env
from app.database.crud.user import user_crud, Session
from app.database.session import pg_session

oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def create_access_token(
    session: Annotated[Session, Depends(pg_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):  # TODO: token type hinting
    """
    OAuth2 compatible token login, set an access token for future requests
    """
    user = user_crud.authenticate(
        session, email=form_data.username, password=form_data.password
    )
    if user and not user_crud.is_active(user):
        HTTP_ERROR(400, "Inactive account")
    if user:
        access_token_expires = timedelta(minutes=float(env.token_expire_minutes))
        access_token = {
            "access_token": encode_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }

        return access_token


def get_current_user(
    session: Annotated[Session, Depends(pg_session)],
    token: Annotated[str, Depends(oauth2)],
):
    token_data = decode_access_token(token)
    current_user = user_crud.get(session, id=token_data.sub)  # type: ignore
    return current_user
