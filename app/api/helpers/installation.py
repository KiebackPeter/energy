from datetime import datetime, timedelta
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session
from app.api.helpers.measurement import fetch_history_of_meter_from_provider

from app.api.helpers.meter import fetch_meters
from app.core.logger import log
from app.database.crud.installation import installation_crud
from app.energy.provider import EnergyProvider


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
