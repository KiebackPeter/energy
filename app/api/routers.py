from fastapi import APIRouter

from app.api.v1.router import api_routers as v1
from app.api.v1.task import router as task

api_router = APIRouter(prefix="/api")

api_router.include_router(v1, prefix="/v1")
# api_router.include_router(functions, prefix="/utils", tags=["Functions"], include_in_schema=False)
api_router.include_router(task, prefix="/task", tags=["Tasks"])
