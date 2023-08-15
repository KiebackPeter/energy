from celery import Celery
from asyncio import get_event_loop
from app.core.logger import env
from .tasks import update_with_remote_meters, update_with_remote_measurements

celery = Celery(__name__, broker=env.broker_url, backend=env.broker_url)

loop = get_event_loop()

@celery.task(name="sync_meters", ignore_result=False)
def sync_meters(installation_id: int, name: str, key: str):
    return loop.run_until_complete(update_with_remote_meters(installation_id, name, key))

@celery.task(name="sync_installation", ignore_result=False)
def sync_installation(installation_id: int, name: str, key: str):
    return loop.run_until_complete(update_with_remote_measurements(installation_id, name, key))
