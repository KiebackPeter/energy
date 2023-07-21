import os
import time

from celery import Celery

from app.energy.provider import EnergyProvider

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="fetch_meters")
def fetch_meters(name, key):
    provider = EnergyProvider(provider_name=name, provider_key=key)
    remote_meters = provider.get_meter_list()
    # write to db
    return remote_meters


@celery.task(name="update_measurements")
def update_measurements():
    
    pass
    