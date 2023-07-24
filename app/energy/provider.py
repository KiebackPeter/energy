from datetime import datetime, timedelta
from app.core.error import HTTP_ERROR
from app.core.logger import log
from app.database.session import use_db
from app.database.crud.meter import meter_crud
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.models.installation import InstallationModel
from app.database.models.meter import MeterModel
from app.energy.adapters import adapter, energiemissie, joulz, kenter
from app.schemas.channel import ChannelWithMeasurements
from app.schemas.meter import MeterCreateDTO


class EnergyProvider:
    """A service to work with different sorts of BaseAdapters"""

    def __init__(self, installation: InstallationModel):

        self.installation = installation
        self._session = use_db()

        if self.installation.provider_name and self.installation.provider_key:
            self.adapter = self.__give_adapter()

            log.info("installation: %s adapter: %s",
                     self.installation.name, self.adapter.__class__.__name__)

    @property
    def meters(self):
        return self.update_meter_list()

    def __give_adapter(self) -> adapter.BaseAdapter:
        """Give adapter for the provider"""

        match self.installation.provider_name:
            case "energiemissie":
                return energiemissie.EnergiemissieAdapter(self.installation.provider_name)
            case "joulz":
                return joulz.JoulzAdapter(self.installation.provider_name)
            # case "fudura":
            #     return fudura.FuduraAdapter(self.installation.provider_name)
            # case "tums":
            #     return tums.TumsAdapter(self.installation.provider_name)
            case "kenter":
                return kenter.KenterAdapter(self.installation.provider_name)
            case _:
                return HTTP_ERROR(
                    404,
                    f"We do not support: {self.installation.provider_name} as energy provider",
                )

    async def update_meter_list(self) -> list[MeterModel]:
        """Uses the adapter's method to get a meter list"""

        new_meters = []
        local_meters = []
        remote_meters: list[MeterModel] = await self.adapter.fetch_meter_list()

        for meter in remote_meters:
            local_meter = meter_crud.get_by_source_id(
                self._session, meter.source_id)

            match local_meter:
                case None:
                    new_meters.append(meter_crud.create(
                        self._session, meter, self.installation.id))
                case _:
                    local_meters.append(local_meter)

        log.info(
            "%s: | %s remote meter(s) | %s local meter(s) | %s new meter(s)",
            self.installation.name,
            len(remote_meters),
            len(local_meters),
            len(new_meters),
        )

        return remote_meters

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
                measurement_crud.create(
                    self._session, meausurement, local_channel.id)
            except Exception as err:
                log.critical("%s", err)
                continue

    async def get_day_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a day"""

        day_measurements_per_channel = await self.adapter.fetch_day_measurements(
            meter.source_id, date
        )
        for raw_channel in day_measurements_per_channel:
            self.__write_measurements(meter.id, raw_channel)

        return day_measurements_per_channel

    async def get_month_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Returns measurement objects from a meter on a speficic month"""
        month_measurements_per_channel = await self.adapter.fetch_month_measurements(
            meter.source_id, date
        )
        for raw_channel in month_measurements_per_channel:
            self.__write_measurements(meter.id, raw_channel)

        return month_measurements_per_channel

    async def update_meter_measurements(
        self,
        meter: MeterModel,
    ):
        log.info(
            "updating measurements for meter: %s id: %s",
            meter.name,
            meter.id
        )

        today = datetime.today()
        latest_known = today - timedelta(days=(365 * 5))

        for channel in meter.channels:
            latest = measurement_crud.latest_measurement(
                self._session, channel.id)

            if latest.timestamp > latest_known:
                latest_known = latest.timestamp

        num_months = (
            (today.year - latest_known.year) * 12 +
            (today.month - latest_known.month) + 1
        )

        for _ in range(num_months):
            await self.get_month_measurements(meter.source_id, latest_known)
            _, days_in_month = monthrange(
                latest_known.year, latest_known.month)
            latest_known = latest_known.replace(
                day=days_in_month) + timedelta(days=1)

        return "done"
