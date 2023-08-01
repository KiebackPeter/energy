from calendar import monthrange
from datetime import datetime, timedelta
from app.core.error import HTTP_ERROR
from app.core.logger import log
from app.database.session import session
from app.database.crud.meter import meter_crud
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.models.meter import MeterModel
from app.energy.adapters import energiemissie, joulz, kenter
from app.schemas.channel import ChannelWithMeasurements


class EnergyProvider:
    """A service to work with different sorts of BaseAdapters"""

    def __init__(self, installation_id: int, provider_name: str, provider_key: str):
        self.installation_id = installation_id

        self.api_name = provider_name
        self.api_key = provider_key

        self._session = session
        self._adapter = self.adapter

        log.info("energyprovider used: %s", self.api_name)

    @property
    def adapter(self):
        """Give adapter for the provider"""

        match self.api_name:
            case "energiemissie":
                return energiemissie.EnergiemissieAdapter(self.api_key)
            case "joulz":
                return joulz.JoulzAdapter(self.api_key)
            # case "fudura":
            #     return fudura.FuduraAdapter(self.installation.api_key)
            # case "tums":
            #     return tums.TumsAdapter(self.installation.api_key)
            case "kenter":
                return kenter.KenterAdapter(self.api_key)
            case _:
                return HTTP_ERROR(
                    404,
                    f"We do not support: {self.api_name} as energy provider",
                )

    async def update_meter_list(self):
        """Uses the adapter's method to get a meter list"""

        new_meters: list[MeterModel] = []
        local_meters: list[MeterModel] = []
        remote_meters = await self._adapter.fetch_meter_list()

        for meter in remote_meters:
            local_meter = meter_crud.get_by_source_id(self._session, meter.source_id)
            if local_meter is None:
                new_meter = meter_crud.create(
                    self._session, meter, self.installation_id
                )
                new_meters.append(new_meter)
            else:
                local_meters.append(local_meter)

        log.info(
            "installation_id: %s | %s remote meter(s) | %s local meter(s) | %s new meter(s)",
            self.installation_id,
            len(remote_meters),
            len(local_meters),
            len(new_meters),
        )

        return local_meters + new_meters

    def __write_measurements(
        self,
        meter_id: int,
        channel_data: ChannelWithMeasurements,
    ):
        """
        write measurements for each given channel for the meter
        """

        local_channel = channel_crud.get_by_channel_name_and_meter(
            self._session, channel_data.channel_name, meter_id
        )
        log.info(
            "writting %s measurements to channel_id: %s",
            len(channel_data.measurements),
            local_channel.id,
        )
        for meausurement in channel_data.measurements:
            # TODO correct execpt and callback
            try:
                measurement_crud.create(self._session, meausurement, local_channel.id)
            except Exception as err:
                log.critical("%s", err)
                continue
        self._session.commit()

    async def get_day_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a day"""

        day_measurements_per_channel = await self._adapter.fetch_day_measurements(
            meter.source_id, date
        )
        for raw_channel in day_measurements_per_channel:
            self.__write_measurements(meter.id, raw_channel)

        return day_measurements_per_channel

    async def get_month_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Returns measurement objects from a meter on a speficic month"""
        month_measurements_per_channel = await self._adapter.fetch_month_measurements(
            meter.source_id, date
        )
        for raw_channel in month_measurements_per_channel:
            self.__write_measurements(meter.id, raw_channel)

        return month_measurements_per_channel

    async def update_meter_measurements(
        self,
        meter: MeterModel,
    ):
        log.info("updating measurements for meter: %s id: %s", meter.name, meter.id)

        last_known = datetime.today() - timedelta(days=(365 * 5))
        
        # TODO ugly check for latest known channel measurements
        for meter in meter_crud.get_by_id_with_channels(self._session, meter.id):
            for channel in meter.channels:
                latest_check = measurement_crud.latest_channel_measurement(
                    self._session, channel.id
                )
                if latest_check is not None:
                    last_known = latest_check

        today = datetime.today()
        num_months = (
            (today.year - last_known.year) * 12 + (today.month - last_known.month) + 1
        )
        if num_months > 1:
            for _ in range(num_months):
                _ = await self.get_month_measurements(meter, last_known)
                _, days_in_month = monthrange(last_known.year, last_known.month)
                last_known = last_known.replace(day=days_in_month) + timedelta(days=1)

            return f"{meter.name} is up-to-date "
        else:
            num_days = today - last_known
            for _ in range(num_days.days):
                _ = await self.get_day_measurements(meter, last_known)
                last_known += timedelta(days=1)

            return f"{meter.name} is up-to-date "
