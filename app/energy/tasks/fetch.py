from datetime import datetime, timedelta
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session
from app.api.helpers.measurement import fetch_history_of_meter_from_provider

from app.api.helpers.meter import fetch_meters
from app.core.logger import log
from app.database.crud.installation import installation_crud
from app.energy.provider import EnergyProvider

from sqlalchemy.orm import Session
from app.database.crud.meter import meter_crud
from app.database.models.meter import MeterModel
from app.energy.provider import EnergyProvider
from app.core.logger import log

from calendar import monthrange
from datetime import datetime, timedelta
from fastapi import BackgroundTasks

from sqlalchemy.orm import Session

from app.core.logger import log
from app.database.models.meter import MeterModel
from app.energy.provider import EnergyProvider


async def fetch_history_of_meter_from_provider(
    session: Session, meter: MeterModel, provider: EnergyProvider
):
    log.info(
        "looking for all know measurements from past 5 years for meter id: %s",
        meter.name,
    )

    today = datetime.today()
    from_date: datetime = today - timedelta(days=(365 * 5))

    num_months = (
        (today.year - from_date.year) * 12 + (today.month - from_date.month) + 1
    )

    for _ in range(num_months):
        await provider.get_month_measurements(session, meter, from_date)

        _, days_in_month = monthrange(from_date.year, from_date.month)
        from_date = from_date.replace(day=days_in_month) + timedelta(days=1)

    return "done"

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


async def sync_installations(session: Session, tasks: BackgroundTasks):
    yesterday = datetime.today() - timedelta(days=1)
    all_installations = installation_crud.get_multi(session)

    for installation in all_installations:
        if installation.provider_name and installation.provider_key:
            provider = EnergyProvider(
                installation.provider_name, installation.provider_key
            )
            local_meters, new_meters = await fetch_meters(
                session, installation.id, provider
            )
            for new_meter in new_meters:
                if new_meter:
                    tasks.add_task(
                        fetch_history_of_meter_from_provider,
                        session,
                        new_meter,
                        provider,
                    )
            # for local_meter in local_meters:
            #     if local_meter:
            #         tasks.add_task(
            #             provider.fetch_day_measurements, session, local_meter, yesterday
            #         )

    return "Tasks are running in background"
