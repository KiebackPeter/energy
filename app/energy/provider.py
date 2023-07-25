from calendar import monthrange
from datetime import datetime, timedelta
from app.core.error import HTTP_ERROR
from app.core.logger import log
from app.database.session import SessionLocal
from app.database.crud.meter import meter_crud
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.models.meter import MeterModel
from app.energy.adapters import energiemissie, joulz, kenter
from app.schemas.channel import ChannelWithMeasurements
from app.schemas.meter import MeterCreateDTO

local_session = SessionLocal()


class EnergyProvider:
    """A service to work with different sorts of BaseAdapters"""

    def __init__(self, installation_id: int, provider_name: str, provider_key: str):
        self.installation_id = installation_id

        self.api_name = provider_name
        self.api_key = provider_key

        self._session = self.session
        self._adapter = self.adapter

        log.info("energyprovider used: %s", self.api_name)

    @property
    def session(self):
        return local_session

    @property
    def adapter(self):
        """Give adapter for the provider"""

        match self.api_name:
            case "energiemissie":
                return energiemissie.EnergiemissieAdapter(self.api_key)
            case "joulz":
                return joulz.JoulzAdapter(self.api_key)
            # case "fudura":
            #     return fudura.FuduraAdapter(self.installation.provider_name)
            # case "tums":
            #     return tums.TumsAdapter(self.installation.provider_name)
            case "kenter":
                return kenter.KenterAdapter(self.api_key)
            case _:
                return HTTP_ERROR(
                    404,
                    f"We do not support: {self.api_name} as energy provider",
                )

    @property
    def meters(self):
        return self.update_meter_list()

    async def update_meter_list(self) -> list[MeterModel]:
        """Uses the adapter's method to get a meter list"""

        new_meters: list[MeterModel] = []
        local_meters: list[MeterModel] = []
        remote_meters: list[MeterCreateDTO] = await self._adapter.fetch_meter_list()

        for meter in remote_meters:
            local_meter = meter_crud.get_by_source_id(self._session, meter.source_id)

            if local_meter is None:
                new_meters.append(
                    meter_crud.create(self._session, meter, self.installation_id)
                )
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

    async def __write_measurements(
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

    async def get_day_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a day"""

        day_measurements_per_channel = await self._adapter.fetch_day_measurements(
            meter.source_id, date
        )
        for raw_channel in day_measurements_per_channel:
            await self.__write_measurements(meter.id, raw_channel)

        return day_measurements_per_channel

    async def get_month_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Returns measurement objects from a meter on a speficic month"""
        month_measurements_per_channel = await self._adapter.fetch_month_measurements(
            meter.source_id, date
        )
        for raw_channel in month_measurements_per_channel:
            await self.__write_measurements(meter.id, raw_channel)

        return month_measurements_per_channel

    async def update_meter_measurements(
        self,
        meter: MeterModel,
    ):
        log.info("updating measurements for meter: %s id: %s", meter.name, meter.id)

        # NOTE checks only the first channel
        latest_known = measurement_crud.latest_measurement(
            self._session, meter.channels[0].id
        )

        today = datetime.today()
        num_months = (
            (today.year - latest_known.year) * 12
            + (today.month - latest_known.month)
            + 1
        )
        for _ in range(num_months):
            await self.get_month_measurements(meter, latest_known)
            _, days_in_month = monthrange(latest_known.year, latest_known.month)
            latest_known = latest_known.replace(day=days_in_month) + timedelta(days=1)

        return {"status": True}
