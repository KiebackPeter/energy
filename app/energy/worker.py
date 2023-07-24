import time
from celery.app import Celery
from app.core.logger import log, env
from app.database.models.installation import InstallationModel
from app.database.models.meter import MeterModel

# from app.core.logger import log

from app.energy.provider import EnergyProvider

celery = Celery(__name__, broker=env.broker_url, backend=env.broker_url)


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


@celery.task(name="get_updates")
async def get_updates(provider: EnergyProvider):
    
    remote_meters = await provider.update_meter_list()

    for meter in remote_meters:
        await provider.update_meter_measurements(meter)

    log.info("updated %s meter(s)", len(remote_meters))
