from datetime import datetime
from fastapi import BackgroundTasks

from sqlalchemy.orm import Session

from app.core.error import HTTP_ERROR
from app.core.logger import log
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.models.meter import MeterModel
from app.database.models.meter import MeterModel
from app.energy.adapters import adapter, energiemissie, joulz, kenter
from app.schemas.channel import ChannelWithMeasurements
from app.schemas.meter import MeterCreateDTO


class EnergyProvider:
    """A service to work with different sorts of BaseAdapters"""

    def __init__(self, source_provider: str | None, provider_key: str | None):
        if source_provider and provider_key:
            self._source_provider = source_provider.lower()
            self._provider_key = provider_key
            self.adapter = self.give_adapter()

            log.info("Energy adapter used: %s", self.adapter.__class__.__name__)

    def give_adapter(self) -> adapter.BaseAdapter:
        """Give adapter for the provider"""

        match self._source_provider:
            case "energiemissie":
                return energiemissie.EnergiemissieAdapter(self._provider_key)
            case "joulz":
                return joulz.JoulzAdapter(self._provider_key)
            # case "fudura":
            #     return fudura.FuduraAdapter(self._provider_key)
            # case "tums":
            #     return tums.TumsAdapter(self._provider_key)
            case "kenter":
                return kenter.KenterAdapter(self._provider_key)
            case _:
                return HTTP_ERROR(
                    404,
                    f"We do not support: {self._source_provider} as energy provider",
                )

    async def write_measurements(
        self,
        session: Session,
        meter_id: int,
        channel_with_measurements: ChannelWithMeasurements,
    ):
        """
        write measurements for each given channel for the meter
        """

        local_channel = channel_crud.get_by_channel_name_and_meter(
            session, channel_with_measurements.channel_name, meter_id
        )
        log.info(
            "writting %s measurements to channel_id: %s",
            len(channel_with_measurements.measurements),
            local_channel.id,
        )
        for meausurement in channel_with_measurements.measurements:
            try:
                measurement_crud.create(session, meausurement, local_channel.id)
            except:
                log.critical("dubbel for channel %s", local_channel.id)
                continue

    async def get_meter_list(self) -> list[MeterCreateDTO]:
        """Uses the adapter's method to get a meter list"""

        meter_list = await self.adapter.get_meter_list()

        return meter_list

    async def fetch_day_measurements(
        self, session: Session, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a day"""

        day_measurements_per_channel = await self.adapter.get_day_measurements(
            meter.source_id, date
        )
        for raw_channel in day_measurements_per_channel:
            await self.write_measurements(session, meter.id, raw_channel)

        return day_measurements_per_channel

    async def get_month_measurements(
        self, session: Session, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Returns measurement objects from a meter on a speficic month"""
        month_measurements_per_channel = await self.adapter.get_month_measurements(
            meter.source_id, date
        )
        if len(month_measurements_per_channel) > 0:
            for raw_channel in month_measurements_per_channel:
                await self.write_measurements(session, meter.id, raw_channel)

        return month_measurements_per_channel
