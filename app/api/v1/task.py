from fastapi import APIRouter, Depends
from celery.result import AsyncResult
from pydantic import BaseModel
from app.energy import worker

from app.api.dependencies.installation import get_all_installations
from app.api.dependencies.measurements import (
    delete_measurements_range,
    update_day_measurement_from_provider,
    update_month_measurement_from_provider,
)

router = APIRouter()

# TODO https://github.com/testdrivenio/fastapi-celery/tree/master


class TaskOut(BaseModel):
    id: str
    status: str


def _to_task_out(req: AsyncResult) -> TaskOut:
    return TaskOut(id=req.task_id, status=req.status)


@router.get("/{task_id}/status")
def status(task_id: str) -> TaskOut:
    req = AsyncResult(task_id)
    return _to_task_out(req)


@router.get("/updates")
async def fetch_measurements_for_all_installations(
    installations=Depends(get_all_installations),
):
    tasks = []

    for installation in installations:
        task = await worker.get_updates.delay(installation)
        tasks.append(task)



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
