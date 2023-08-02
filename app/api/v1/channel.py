from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.channel import channel_of_meter_by_id
from app.database.models.channel import ChannelModel
from app.database.crud.channel import channel_crud
from app.database.session import pg_session
from app.schemas.channel import ChannelUpdateDTO

router = APIRouter()


@router.put("/{channel_id}/qanteon_name")
async def put_channel_qanteon_name(
    updated_obj: ChannelUpdateDTO,
    channel: Annotated[ChannelModel, Depends(channel_of_meter_by_id)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_channel = channel_crud.update(session, (channel.__dict__), updated_obj)
    return updated_channel.__dict__
