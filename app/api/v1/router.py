from fastapi import APIRouter

from app.api.v1.auth import router as auth
from app.api.v1.channel import router as channel
from app.api.v1.installation import router as installation
from app.api.v1.measurements import router as measurements
from app.api.v1.meter import router as meter
from app.api.v1.user import router as user

api_routers = APIRouter()

api_routers.include_router(auth, prefix="/auth", tags=["Auth"])
api_routers.include_router(user, prefix="/user", tags=["User"])
api_routers.include_router(installation, prefix="/installation", tags=["Installation"])
api_routers.include_router(meter, prefix="/energy/meter", tags=["Energy  | Meter"])
api_routers.include_router(channel, prefix="/energy/channel", tags=["Energy  | Channel"])
api_routers.include_router(measurements, prefix="/energy/measurements", tags=["Energy  | Measurements"])  # pylint: disable=line-too-long
