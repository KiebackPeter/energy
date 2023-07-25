from celery import Celery
from asyncio import run, create_task
from app.core.logger import log, env
from app.database.models.meter import MeterModel

# from app.core.logger import log

from app.energy.provider import EnergyProvider


celery = Celery(__name__, broker=env.broker_url, backend=env.broker_url)



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


@celery.task(name="get_updates", ignore_result=True)
def get_updates(installation_id: int, name: str, key: str):
    provider = EnergyProvider(installation_id, name, key)
    background_tasks = set()
    
    response = run(provider.update_meter_list(), debug=True)
    try:
        for meter in response:
            create_task(provider.update_meter_measurements(meter))

    except Exception as exception:
        print(exception)
    
    return {"status": True}
