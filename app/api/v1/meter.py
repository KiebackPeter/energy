from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.installation import of_user, with_owner

from app.api.dependencies.meter import meter_of_installation_by_id
from app.database.models.installation import InstallationModel
from app.database.models.meter import MeterModel
from app.database.session import pg_session
from app.schemas.meter import MeterCreateDTO, MeterPublic, MeterUpdateDTO
from app.database.crud.meter import meter_crud

router = APIRouter()


@router.post("")
def new_meter(
    create_data: MeterCreateDTO,
    installation: Annotated[InstallationModel, Depends(with_owner)],
    session: Annotated[Session, Depends(pg_session)],
):
    meter = meter_crud.create(session, create_data, installation.id)

    return meter


@router.get("/all")
def all_installation_meters(
    installation: Annotated[InstallationModel, Depends(of_user)],
):
    # TODO return meter with channels
    return installation.meters


@router.get("/{meter_id}")
def get_meter_by_id(
    session: Annotated[Session, Depends(pg_session)],
    meter: Annotated[MeterModel, Depends(meter_of_installation_by_id)],
):

    return meter_crud.get_by_id_with_channels(session, meter.id)

@router.get("/{meter_id}/channels")
def all_meter_channels(
    session: Annotated[Session, Depends(pg_session)],
    meter: Annotated[MeterModel, Depends(meter_of_installation_by_id)],
):
    channels = meter_crud.get_by_id_with_channels(session, meter.id)
    return channels

@router.put("/{meter_id}", response_model=MeterPublic)
def put_meter_by_id(
    update_data: MeterUpdateDTO,
    meter: Annotated[MeterModel, Depends(meter_of_installation_by_id)],
    session: Annotated[Session, Depends(pg_session)],
):
    updated_meter = meter_crud.update(session, meter, update_data)

    return updated_meter.__dict__
