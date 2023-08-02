from fastapi.encoders import jsonable_encoder

from app.database.models.channel import ChannelModel
from app.schemas.channel import ChannelCreateDTO, ChannelUpdateDTO
from app.database.crud.base_crud  import Session, CRUDBase, select, insert  # , log,


class CRUDChannel(CRUDBase[ChannelModel, ChannelCreateDTO, ChannelUpdateDTO]):
    def create(self, session: Session, create_obj: ChannelCreateDTO, meter_id: int):
        channel_data = jsonable_encoder(create_obj)
        channel_data["meter_id"] = meter_id
        new_channel = session.scalars(
            insert(self.model).values(channel_data).returning(self.model)
        ).one()
        session.commit()
        return new_channel

    def get_by_channel_name_and_meter(
        self, session: Session, channel_name: str, meter_id: int
    ):
        channel = session.scalars(
            select(self.model).filter_by(meter_id=meter_id, name=channel_name)
        ).one_or_none()
        if channel is None:
            log.info("creating channel: %s for point %s", channel_name, meter_id)

            channel = self.create(
                session,
                create_obj=ChannelCreateDTO(name=channel_name),
                meter_id=meter_id,
            )
        return channel


channel_crud = CRUDChannel(ChannelModel)
