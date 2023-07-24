from typing import Annotated
from fastapi import Depends
from app.api.dependencies.installation import of_user

from app.core.error import HTTP_ERROR
from app.database.crud.channel import channel_crud, Session
from app.database.models.channel import ChannelModel
from app.database.models.installation import InstallationModel
from app.database.session import use_db


# def create_channel(
#     create_data: ChannelCreateDTO,
#     meter=Depends(meter_of_installation_by_id),
#     session=Depends(use_db),
# ):
#     new_channel = channel_crud.create(session, create_data, meter.id)

#     return new_channel


def channel_of_meter_by_id(
    channel_id: int,
    session: Annotated[ Session, Depends(use_db)],
    installation: Annotated[ InstallationModel, Depends(of_user)],
) -> ChannelModel:
    channel = channel_crud.get(session, id=channel_id)
    for meter in installation.meters:
        if channel.meter_id == meter.id:
            return channel

    return HTTP_ERROR(400, "You do not have enough privileges")