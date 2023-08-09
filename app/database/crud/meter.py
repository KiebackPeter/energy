from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload, Session
from app.database.models.meter import MeterModel
from app.schemas.meter import MeterCreateDTO, MeterUpdateDTO

from app.database.crud.base_crud import Session, CRUDBase  # ,log


class CRUDMeter(CRUDBase[MeterModel, MeterCreateDTO, MeterUpdateDTO]):
    def create(
        self, session: Session, create_obj: MeterCreateDTO, installation_id: int
    ):
        meter_data = jsonable_encoder(create_obj)
        meter_data["installation_id"] = installation_id
        new_meter = session.scalars(
            insert(self.model).values(meter_data).returning(self.model)
        ).one()
        session.commit()
        return new_meter

    def get_by_id_with_channels(self, session: Session, meter_id: int):
        return session.scalar(
            select(MeterModel)
            .where(MeterModel.id == meter_id)
            .options(selectinload(MeterModel.channels))
        )

    def get_by_source_id(self, session: Session, source_id: str):
        return session.scalars(
            select(self.model).filter_by(source_id=source_id)
        ).one_or_none()


meter_crud = CRUDMeter(MeterModel)
