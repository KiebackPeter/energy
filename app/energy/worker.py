import os
import time

from celery import Celery
from app.database.models.meter import MeterModel
from app.core.logger import log

from app.energy.provider import EnergyProvider

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="update_meters")
async def update_meters(provider: EnergyProvider):
    remote_meters = await provider.update_meter_list()

    return remote_meters


@celery.task(name="update_measurements")
async def update_measurements(provider: EnergyProvider, meters: list[MeterModel]):

    for meter in meters:
        await provider.update_meter_measurements(meter)

    log.info("updated %s meter(s)", len(meters))

    return meters
