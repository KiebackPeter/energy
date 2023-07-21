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
