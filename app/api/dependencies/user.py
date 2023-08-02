from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.core.error import HTTP_ERROR
from app.database.crud.user import user_crud
from app.database.models.user import UserModel
from app.database.session import pg_session
from app.schemas.user import UserPublic


# Guard dependencies


def current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)],
):
    if not current_user.is_active:
        HTTP_ERROR(400, "Inactive account")

    return current_user


def current_active_superuser(
    current_user: Annotated[UserModel, Depends(current_active_user)],
):
    if not current_user.is_superuser:
        HTTP_ERROR(400, "You do not have enough privileges")

    return current_user


# SU functions


def get_all_users(
    skip: int | None,
    limit: int | None,
    current_user: Annotated[UserModel, Depends(current_active_superuser)],
    session: Annotated[Session, Depends(pg_session)],
):
    users = user_crud.get_multi(session, skip=skip, limit=limit)

    return users


def get_user_by_id(
    user_id: int,
    current_user: Annotated[UserModel, Depends(current_active_superuser)],
    session: Annotated[Session, Depends(pg_session)],
):
    user = user_crud.get(session, id=user_id)

    return user


def update_user_by_id(
    user_in: UserPublic,
    user: Annotated[UserModel, Depends(get_user_by_id)],
    session: Annotated[Session, Depends(pg_session)],
):
    return user_crud.update(session, user, user_in)
