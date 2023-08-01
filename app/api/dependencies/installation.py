from typing import Annotated
from fastapi import Depends

from app.api.dependencies.user import current_active_superuser, current_active_user
from app.core.error import HTTP_ERROR
from app.database.crud.installation import installation_crud, Session
from app.database.models.installation import InstallationModel
from app.database.models.user import UserModel
from app.database.session import pg_session
from app.schemas.installation import InstallationUpdateDTO


# Guard dependencies


def of_user(
    session: Annotated[Session, Depends(pg_session)],
    current_user: Annotated[UserModel, Depends(current_active_user)],
    installation_id: int | None = None,
):
    # BUG doesnt pick up installation id?
    if installation_id and current_user.is_superuser:
        installation = installation_crud.get_by(session, id=installation_id)
        return installation

    elif current_user.installation_id:
        installation = installation_crud.get_with_meters(
            session, current_user.installation_id
        )
        return installation


def with_owner(
    current_user: Annotated[UserModel, Depends(current_active_user)],
    installation: Annotated[InstallationModel, Depends(of_user)],
):
    if not current_user.is_superuser:
        if not current_user.email == installation.owner_email:
            HTTP_ERROR(400, "You do not have enough privileges")

    return installation

# SU dependencies


def get_all_installations(
    session: Annotated[Session, Depends(pg_session)],
    current_user: Annotated[UserModel, Depends(current_active_superuser)],
):
    installations = installation_crud.filter_by(session)

    return installations


def get_installation_by_id(
    installation_id: int,
    session: Annotated[Session, Depends(pg_session)],
    current_user: Annotated[UserModel, Depends(current_active_superuser)],
):
    installation = installation_crud.get_by(session, id=installation_id)

    return installation


def update_installation_by_id(
    installation_id: int,
    update_data: InstallationUpdateDTO,
    session: Annotated[Session, Depends(pg_session)],
    current_user: Annotated[UserModel, Depends(current_active_superuser)],
):
    installation = installation_crud.get_by(session, id=installation_id)
    updated_installation = installation_crud.update(session, installation, update_data)

    return updated_installation


# def add_user_to_installation(
# #     user_id: int,
# #     installation=Depends(with_owner),
# #     session=Depends(pg_session),
# ):
# installation_crud.connect_user(session, user_id, installation)
#     return "not implemented"
