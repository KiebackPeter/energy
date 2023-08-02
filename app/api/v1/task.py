from fastapi import APIRouter, Depends
from celery.result import AsyncResult
from app.database.models.installation import InstallationModel
from app.energy import worker

from app.api.dependencies.installation import get_all_installations, with_owner
router = APIRouter()

# TODO https://github.com/testdrivenio/fastapi-celery/tree/master


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
