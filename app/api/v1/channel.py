from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.channel import channel_of_meter_by_id
from app.api.dependencies.meter import meter_of_installation_by_id
from app.database.models.channel import ChannelModel
from app.database.models.meter import MeterModel
from app.database.crud.channel import channel_crud
from app.database.session import pg_session
from app.schemas.channel import ChannelUpdateDTO

router = APIRouter()


@router.get("/{meter_id}/all")
def all_channels(
    meter: Annotated[MeterModel, Depends(meter_of_installation_by_id)],
):
    return meter.channels


@router.put("/{channel_id}/qanteon_name")
def put_channel_qanteon_name(
    updated_obj: ChannelUpdateDTO,
    channel: Annotated[ChannelModel, Depends(channel_of_meter_by_id)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_channel = channel_crud.update(session, channel, updated_obj)

    return updated_channel
