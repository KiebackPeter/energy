from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.implementations.base_crud import AsyncSession, CRUDBase  # ,log
from app.database.models.installation import InstallationModel
from app.database.models.user import UserModel
from app.schemas.installation import InstallationCreateDTO, InstallationUpdateDTO


class CRUDInstallation(
    CRUDBase[InstallationModel, InstallationCreateDTO, InstallationUpdateDTO]
):
    async def create(
        self,
        session: AsyncSession,
        create_obj: InstallationCreateDTO,
        current_user: UserModel,
    ):
        installation_data = jsonable_encoder(create_obj)
        installation_data["owner_email"] = current_user.email

        return await self.do_create(session, installation_data)

    async def get_with_meters(self, session: AsyncSession, installaiton_id: int):
        return await session.scalars(
            select(self.model).options(selectinload(self.model.meters))
        )


# TODO connect multiple users to an installation
# def connect_user(
#     self, session: AsyncSession, user_id: int, installation, current_user: UserModel
# ):
#     user = session.query(UserModel).filter( UserModel.id == user_id).first()
#     installation.users.append(user)
#     session.commit()
#     session.refresh(installation)
#     return {"succes"}


installation_crud = CRUDInstallation(InstallationModel)
