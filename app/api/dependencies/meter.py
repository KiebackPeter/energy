from typing import Annotated
from fastapi import Depends

from app.api.dependencies.installation import (
    of_user,
)
from app.core.error import HTTP_ERROR
from app.database.models.installation import InstallationModel

# Guard dependencies

async def meter_of_installation_by_id(
    meter_id: int,
    installation: Annotated[ InstallationModel, Depends(of_user)],
):
    for meter in installation.meters:
        if meter.id == meter_id:
            return meter
        
    return HTTP_ERROR(400, "You do not have enough privileges")
