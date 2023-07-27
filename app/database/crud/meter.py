from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from app.database.models.meter import MeterModel
from app.schemas.meter import MeterCreateDTO, MeterUpdateDTO

from app.core.implementations.base_crud import AsyncSession, CRUDBase # ,log

class CRUDMeter(CRUDBase[MeterModel, MeterCreateDTO, MeterUpdateDTO]):
    def create(
        self, session: AsyncSession, create_obj: MeterCreateDTO, installation_id: int
    ):
        meter_data = jsonable_encoder(create_obj)
        meter_data["installation_id"] = installation_id

        new_meter = session.scalar(
            insert(self.model).values(meter_data).returning(self.model)
        )

        return new_meter

    def get_by_id_with_channels(self, session: AsyncSession, meter_id: int):
        return session.scalars(
            select(self.model).where(self.model.id == meter_id).options(selectinload(self.model.channels))
        )
    
    def get_by_source_id(
        self, session: AsyncSession, source_id: str
    ):
        return (
            session.query(self.model).filter(self.model.source_id == source_id).first()
        )


meter_crud = CRUDMeter(MeterModel)
