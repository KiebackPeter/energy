from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.core.implementations.base_crud import CRUDBase # ,log
from app.database.models.meter import MeterModel
from app.schemas.meter import MeterCreateDTO, MeterUpdateDTO


class CRUDMeter(CRUDBase[MeterModel, MeterCreateDTO, MeterUpdateDTO]):
    async def create(
        self, session: Session, create_obj: MeterCreateDTO, installation_id: int
    ) -> MeterModel:
        meter_data = jsonable_encoder(create_obj)
        meter_data["installation_id"] = installation_id

        return self.commit(session, database_model=MeterModel(**meter_data))

    async def get_by_source_id(
        self, session: Session, source_id: str
    ) -> MeterModel | None:
        return (
            session.query(self.model).filter(self.model.source_id == source_id).first()
        )


meter_crud = CRUDMeter(MeterModel)
