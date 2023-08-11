from fastapi import APIRouter, Depends
from celery.result import AsyncResult
from pydantic import BaseModel
from app.database.models.installation import InstallationModel
from app.energy import worker

from app.api.dependencies.installation import get_all_installations, with_owner
from app.api.dependencies.measurements import (
    delete_measurements_range,
    update_day_measurement_from_provider,
    update_month_measurement_from_provider,
)

router = APIRouter()


def _to_task_out(req: AsyncResult):
    return {"id": req.task_id, "status": req.status}


@router.get("/{task_id}/status")
async def status(task_id: str):
    req = AsyncResult(task_id)
    return _to_task_out(req)


@router.get("/update/installation/{installation_id}")
def fetch_measurements_for_all_installations(
    installation: InstallationModel = Depends(with_owner),
):
    task = worker.sync_installation.delay(
        installation.id, installation.provider_name, installation.provider_key
    )

    return {"task": _to_task_out(task)}


@router.get("/fetch/{meter_id}/day/{year}/{month}/{day}")
def day_measurements_from_provider(
    day_list=Depends(update_day_measurement_from_provider),
):
    return day_list


@router.get("/fetch/{meter_id}/month/{year}/{month}")
def month_measurement_from_provider(
    month_list=Depends(update_month_measurement_from_provider),
):
    return month_list


@router.delete("/delete/{channel_id}/since/{from_date}")
def delete_all_measurements_since(
    response=Depends(delete_measurements_range),
):
    return response
