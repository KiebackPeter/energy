from asyncio.taskgroups import TaskGroup
from asyncio.tasks import ensure_future, wait_for
from celery import Celery
from app.core.logger import log, env
from app.energy.provider import EnergyProvider
from asyncio import get_event_loop, create_task, gather, sleep

celery = Celery(__name__, broker=env.broker_url, backend=env.broker_url)


async def sync_remote_meters(installation_id, provider: EnergyProvider):
    return


async def fetch_data_async(installation_id: int, name: str, key: str):
    provider = EnergyProvider(installation_id, name, key)

    meters = await provider.update_meter_list()

    for meter in meters:
        await provider.update_meter_measurements(meter)

    return {"msg": f"updated meters: {len(meters}"}


@celery.task(name="sync_installation", ignore_result=False)
def sync_installation(installation_id: int, name: str, key: str):
    loop = get_event_loop()
    return loop.run_until_complete(fetch_data_async(installation_id, name, key))
