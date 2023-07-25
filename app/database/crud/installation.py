from fastapi.encoders import jsonable_encoder
from app.core.implementations.base_crud import Session, CRUDBase # ,log
from app.database.models.installation import InstallationModel
from app.database.models.user import UserModel
from app.schemas.installation import InstallationCreateDTO, InstallationUpdateDTO


class CRUDInstallation(
    CRUDBase[InstallationModel, InstallationCreateDTO, InstallationUpdateDTO]
):
    def create(
        self, session: Session, create_obj: InstallationCreateDTO, current_user: UserModel
    ) -> InstallationModel:
        installation_data = jsonable_encoder(create_obj)
        installation_data["owner_email"] = current_user.email

        new_installation = InstallationModel(**installation_data)
        installation_model = self.commit(session, database_model=new_installation)
        current_user.installation_id = installation_model.id
        session.commit()
        # FIXME this should return an object
        return installation_model


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
