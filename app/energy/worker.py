import time
from asyncio import get_event_loop, create_task
from celery import Celery
from app.core.logger import log, env
from app.database.models.installation import InstallationModel
from app.database.models.meter import MeterModel

# from app.core.logger import log

from app.energy.provider import EnergyProvider

celery = Celery("energy", broker=env.broker_url, backend=env.broker_url)



@celery.task(name="update_meters")
async def update_meters(installation_id: int, name: str, key: str):
    provider = EnergyProvider(installation_id, name, key)

    remote_meters = provider.update_meter_list()

    return remote_meters


@celery.task(name="update_measurements")
def update_measurements(installation_id: int, name: str, key: str, meters: list[MeterModel]):
    provider = EnergyProvider(installation_id, name, key)

    new_measurements = []
    for meter in meters:
        new_measurements.append(provider.update_meter_measurements(meter))

    log.info("updated %s meter(s)", len(meters))

    return new_measurements


@celery.task(name="get_updates")
def get_updates(installation_id: int, name: str, key: str):

    provider = EnergyProvider(installation_id, name, key)

    loop = get_event_loop()
    remote_meters = loop.run_until_complete(provider.update_meter_list())
    print(f"remote_meters: {remote_meters}")
    
    background_tasks = set()

    for meter in remote_meters:
        task = loop.run_until_complete(provider.update_meter_measurements(meter))

        # Add task to the set. This creates a strong reference.
        background_tasks.add(task)

        # To prevent keeping references to finished tasks forever,
        # make each task remove its own reference from the set after
        # completion:
        task.add_done_callback(background_tasks.discard)
    
    return {"status": True}
