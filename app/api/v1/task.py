from fastapi import APIRouter, BackgroundTasks, Depends
from app.api.helpers.installation import sync_installations
from app.api.dependencies.user import current_active_superuser

from app.api.dependencies.measurements import (
    delete_measurements_range,
    update_day_measurement_from_provider,
    update_month_measurement_from_provider,
)
from app.database.session import use_db

router = APIRouter()

# TODO https://github.com/testdrivenio/fastapi-celery/tree/master

@router.get("/daily")
async def fetch_measurements_for_all_installations(
    do: BackgroundTasks,
    session=Depends(use_db),
    superuser=Depends(current_active_superuser),
):
    return await sync_installations(session, do)


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
