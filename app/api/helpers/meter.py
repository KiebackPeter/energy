from sqlalchemy.orm import Session
from app.database.crud.meter import meter_crud
from app.database.models.meter import MeterModel
from app.energy.provider import EnergyProvider
from app.core.logger import log


async def fetch_meters(
    session: Session,
    installation_id: int,
    provider: EnergyProvider,
):
    new_meters: list[MeterModel | None] = []
    local_meters: list[MeterModel | None] = []

    remote_meters = await provider.get_meter_list()

    for meter in remote_meters:
        local_meter = meter_crud.get_by_source_id(session, meter.source_id)
        if not local_meter:
            new_meters.append(meter_crud.create(session, meter, installation_id))
        else:
            local_meters.append(local_meter)

    log.info(
        "%s remote meter(s) | %s local meter(s) | %s new meter(s)",
        len(remote_meters),
        len(local_meters),
        len(new_meters),
    )

    return local_meters, new_meters
