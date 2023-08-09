from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, insert
from app.database.crud.base_crud import Session, CRUDBase  # ,log
from app.database.models.installation import InstallationModel
from app.database.models.user import UserModel
from app.schemas.installation import InstallationCreateDTO, InstallationUpdateDTO


class CRUDInstallation(
    CRUDBase[InstallationModel, InstallationCreateDTO, InstallationUpdateDTO]
):
    def create(
        self,
        session: Session,
        create_obj: InstallationCreateDTO,
        owner_email: str,
    ):
        installation_data = jsonable_encoder(create_obj)
        installation_data["owner_email"] = owner_email

        new_installation = session.scalar(
            insert(self.model).values(installation_data).returning(self.model)
        )
        session.commit()
        return new_installation

    def get_with_meters(self, session: Session, installaiton_id: int):
        return session.scalars(
            select(self.model)
            .filter(self.model.id == installaiton_id)
            .options(selectinload(self.model.meters))
        )


# TODO connect multiple users to an installation
# def connect_user(
#     self, session: Session, user_id: int, installation, current_user: UserModel
# ):
#     user = session.query(UserModel).filter( UserModel.id == user_id).first()
#     installation.users.append(user)
#     session.commit()
#     session.refresh(installation)
#     return {"succes"}


installation_crud = CRUDInstallation(InstallationModel)
