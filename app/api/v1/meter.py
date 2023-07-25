from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.dependencies.installation import with_owner

from app.api.dependencies.meter import meter_of_installation_by_id
from app.database.models.installation import InstallationModel
from app.database.models.meter import MeterModel
from app.database.session import use_db
from app.schemas.meter import MeterCreateDTO, MeterPublic, MeterUpdateDTO
from app.database.crud.meter import meter_crud

router = APIRouter()


@router.post("")
def new_meter(
    create_data: MeterCreateDTO,
    installation: Annotated[InstallationModel, Depends(with_owner)],
    session: Annotated[Session, Depends(use_db)],
):
    meter = meter_crud.create(session, create_data, installation.id)

    return meter.__dict__


@router.get("/all")
def all_installation_meters(
    installation: Annotated[InstallationModel, Depends(with_owner)],
):
    return installation.meters


# TODO get all channels from MeterModel relationship
@router.get("/{meter_id}")
def get_meter_by_id(
    meter: Annotated[MeterModel, Depends(meter_of_installation_by_id)],
):
    return meter.__dict__


@router.put("/{meter_id}", response_model=MeterPublic)
def put_meter_by_id(
    update_data: MeterUpdateDTO,
    meter: Annotated[MeterModel, Depends(meter_of_installation_by_id)],
    session: Annotated[Session, Depends(use_db)],
):
    updated_meter = meter_crud.update(session, meter, update_data)

    return updated_meter.__dict__
