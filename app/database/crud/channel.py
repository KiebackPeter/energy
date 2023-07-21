from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.error import HTTP_ERROR
from app.core.implementations.base_crud import CRUDBase
from app.core.logger import log
from app.database.models.channel import ChannelModel
from app.schemas.channel import ChannelCreateDTO, ChannelUpdateDTO


class CRUDChannel(CRUDBase[ChannelModel, ChannelCreateDTO, ChannelUpdateDTO]):
    def create(
        self, session: Session, create_obj: ChannelCreateDTO, meter_id: int
    ) -> ChannelModel:
        channel_data = jsonable_encoder(create_obj)
        channel_data["meter_id"] = meter_id

        return self.commit(session, database_model=ChannelModel(**channel_data))


    def get_by_channel_name_and_meter(
        self, session: Session, channel_name: str, meter_id: int
    ) -> ChannelModel:
        channel = (
            session.query(self.model)
            .filter(self.model.meter_id == meter_id, self.model.name == channel_name)
            .first()
        )
        if channel is None:
            log.info("creating channel: %s for point %s", channel_name, meter_id)

            channel = self.create(
                session,
                create_obj=ChannelCreateDTO(name=channel_name),
                meter_id=meter_id,
            )
        return channel

    def get_all_by_meter_id(
        self, session: Session, meter_id: int
    ) -> list[ChannelModel]:
        channels = (
            session.query(self.model).filter(self.model.meter_id == meter_id).all()
        )
        if not channels:
            HTTP_ERROR(404, f"No channels found for meter id: {meter_id}")
        return channels


channel_crud = CRUDChannel(ChannelModel)
