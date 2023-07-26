from typing import Annotated
from fastapi import APIRouter, Depends

from app.api.dependencies.installation import (
    of_user,
    with_owner,
)
from app.api.dependencies.user import current_active_user
from app.core.error import HTTP_ERROR
from app.database.models.installation import InstallationModel
from app.database.models.user import UserModel
from app.database.session import pg_session, async_pg_session, AsyncSession, Session
from app.database.crud.installation import installation_crud

from app.schemas.installation import (
    InstallationCreateDTO,
    InstallationPublic,
    InstallationUpdateDTO,
)


router = APIRouter()


@router.post("")
async def new_installation(
    create_data: InstallationCreateDTO,
    user: Annotated[UserModel, Depends(current_active_user)],
    session: Annotated[AsyncSession, Depends(async_pg_session)],
):
    if user.installation_id and not user.is_superuser:
        HTTP_ERROR(406, "You already have an installation")

    return await installation_crud.create(session, create_data, user)



@router.get("")
def get_installation(installation: Annotated[InstallationModel, Depends(of_user)]):
    return installation


@router.put("", response_model=InstallationPublic)
def put_installation_of_user(
    update_data: InstallationUpdateDTO,
    installation: Annotated[InstallationModel, Depends(with_owner)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_installation = installation_crud.update(session, installation, update_data)

    return updated_installation.__dict__


# @router.post("/add_user/")
# def add_user_to_installation(connected_user=Depends(installation.connect_user)):
#     return connected_user.__dict__


# @router.get("/all", response_model=list[InstallationPublic])
# def all_installations(
#     installation_list=Depends(get_all_installations),
# ):
#     return installation_list


# @router.get("/{installation_id}", response_model=InstallationPublic)
# def installation_by_id(
#     found_by_id=Depends(get_installation_by_id),
# ):
#     return found_by_id.__dict__


# @router.put("/{installation_id}", response_model=InstallationPublic)
# def put_installation_by_id(
#     updated_by_id=Depends(update_installation_by_id),
# ):
#     return updated_by_id.__dict__
