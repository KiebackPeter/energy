from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.user import current_active_user
from app.core.error import HTTP_ERROR
from app.database.models.user import UserModel
from app.database.session import pg_session
from app.database.crud.user import user_crud
from app.database.schemas.user import UserCreateDTO, UserPublic, UserUpdateSelfDTO

router = APIRouter()


@router.post("/register", response_model=UserPublic)
def new_user(
    create_data: UserCreateDTO,
    session: Annotated[Session, Depends(pg_session)],
):
    email_check = user_crud.get_credentials(session, email=create_data.email)
    if email_check is not None:
        HTTP_ERROR(400, "This email already registered to a user")

    new_user = user_crud.create(session, create_data)
    return new_user.__dict__


@router.get("", response_model=UserPublic)
def get_user(current_user=Depends(current_active_user)):
    return current_user.__dict__


@router.put("", response_model=UserPublic)
def put_current_user(
    update_data: UserUpdateSelfDTO,
    user: Annotated[UserModel, Depends(current_active_user)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_user = user_crud.update_self(session, user, update_data.dict(exclude_none=True))

    return updated_user.to_dict()

# @router.get("/all", response_model=list[User])
# def all_users(user_list=Depends(get_all_users)):
#     return user_list.__dict__


# @router.get("/{user_id}", response_model=User)
# def user_by_id(found_by_id=Depends(get_user_by_id)):
#     return found_by_id.__dict__


# @router.put("/{user_id}", response_model=User)
# def put_user_by_id(updated_by_id=Depends(update_user_by_id)):
#     return updated_by_id.__dict__
