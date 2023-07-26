from fastapi.encoders import jsonable_encoder
from app.database.models.meter import MeterModel
from app.schemas.meter import MeterCreateDTO, MeterUpdateDTO

from app.core.implementations.base_crud import AsyncSession, CRUDBase # ,log

class CRUDMeter(CRUDBase[MeterModel, MeterCreateDTO, MeterUpdateDTO]):
    def create(
        self, session: AsyncSession, create_obj: MeterCreateDTO, installation_id: int
    ):
        meter_data = jsonable_encoder(create_obj)
        meter_data["installation_id"] = installation_id

        return self.do_create(session, meter_data)

    def get_by_source_id(
        self, session: AsyncSession, source_id: str
    ):
        return (
            session.query(self.model).filter(self.model.source_id == source_id).first()
        )


meter_crud = CRUDMeter(MeterModel)
