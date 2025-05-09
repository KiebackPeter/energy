from calendar import monthrange
from datetime import datetime, timedelta
from asyncpg import DataError

from sqlalchemy.exc import DBAPIError, SQLAlchemyError, StatementError
from app.core.error import HTTP_ERROR
from app.core.logger import log
from app.database.session import session
from app.database.crud.meter import meter_crud
from app.database.crud.channel import channel_crud
from app.database.crud.measurement import measurement_crud
from app.database.models.meter import MeterModel
from app.energy.providers import mock, energiemissie, joulz, kenter
from app.schemas.channel import ChannelWithMeasurements


def energy_provider_factory(provider_name: str, api_key: str):
    match provider_name:
        case "mock":  # test / demo adapter
            return mock.MockAdapter(api_key)
        case "energiemissie":
            return energiemissie.EnergiemissieAdapter(api_key)
        case "joulz":
            return joulz.JoulzAdapter(api_key)
        # case "fudura":
        #     return fudura.FuduraAdapter(allation.api_api_key)
        # case "tums":
        #     return tums.TumsAdapter(allation.api_api_key)
        case "kenter":
            return kenter.KenterAdapter(api_key)
        case _:
            return HTTP_ERROR(
                404,
                f"We do not support: {provider_name} as energy provider",
            )


class EnergyProvider:
    """A service to work with different sorts of BaseProviders"""

    def __init__(self, installation_id: int, provider_name: str, provider_key: str):
        self.installation_id = installation_id

        self._session = session
        self._provider = energy_provider_factory(provider_name, provider_key)

        log.info(
            "energyprovider used: %s for instalation_id: %s",
            provider_name,
            installation_id,
        )

    async def update_meter_list(self):
        """Uses the adapter's method to get a meter list"""

        new_meters: list[MeterModel] = []
        local_meters: list[MeterModel] = []
        remote_meters = await self._provider.fetch_meter_list()

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
            try:
                measurement_crud.create(self._session, meausurement, local_channel.id)
            except (SQLAlchemyError, DBAPIError, StatementError, DataError):
                session.rollback()

        channel_crud.put(
            self._session,
            local_channel,
            {"latest_measurement": channel_data.measurements[-1].timestamp},
        )

    async def get_day_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Uses the adapter's method to get a measuement list of a day"""

        day_measurements_per_channel = await self._provider.fetch_day_measurements(
            meter.source_id, date
        )
        for raw_channel in day_measurements_per_channel:
            self.__write_measurements(meter.id, raw_channel)

        return day_measurements_per_channel

    async def get_month_measurements(
        self, meter: MeterModel, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Returns measurement objects from a meter on a speficic month"""
        month_measurements_per_channel = await self._provider.fetch_month_measurements(
            meter.source_id, date
        )
        for raw_channel in month_measurements_per_channel:
            self.__write_measurements(meter.id, raw_channel)

        return month_measurements_per_channel

    async def update_meter_measurements(
        self,
        meter: MeterModel,
    ):
        """
        Check most recent 'local' measurement from channels
        and,
        fetch measurements from then or start 5 years back.
        """
        log.info("updating measurements for meter: %s id: %s", meter.name, meter.id)

        today = datetime.today()
        five_years_ago = today - timedelta(days=365 * 5)
        last_known = five_years_ago.replace(month=1, day=1, hour=0, minute=0, second=0)

        meter_with_channels = meter_crud.get_by_id_with_channels(
            self._session, meter.id
        )
        if meter_with_channels and meter_with_channels.channels is not None:
            for channel in meter.channels:
                latest_check = datetime.fromtimestamp(channel.latest_measurement)
                # TODO fix, now checking only for most recent, missing, known measurement of channels
                if latest_check is not None and latest_check > last_known:
                    print(f"FOUND LAST_KOWN: {last_known}")
                    last_known = latest_check

        num_months = (
            (today.year - last_known.year) * 12 + (today.month - last_known.month) + 1
        )
        for _ in range(num_months):
            _ = await self.get_month_measurements(meter, last_known)
            _, days_in_month = monthrange(last_known.year, last_known.month)
            last_known = last_known.replace(day=days_in_month) + timedelta(days=1)
            
        self._session.commit()
        
        return f"{meter.name} is up-to-date"
