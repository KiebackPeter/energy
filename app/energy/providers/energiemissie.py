from datetime import datetime

from app.core.logger import log
from app.energy.providers.base_provider import BaseProvider
from app.schemas.channel import ChannelWithMeasurements
from app.schemas.measurements import MeasurementCreateDTO
from app.schemas.meter import MeterCreateDTO


class EnergiemissieAdapter(BaseProvider):
    """A concrete implemetation working with the energiemissie API"""

    def __init__(self, provider_key: str) -> None:
        super().__init__({"x-api-key": provider_key})
        self.base_url = "https://mijnenergiemissie.nl/webservice/v2"

    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        """Returns all available meters from endpoint in meter objects"""

        raw_meter_list = await self.make_request(self.base_url + "/meters")

        meter_objects: list[MeterCreateDTO] = []
        for raw_meter in raw_meter_list:
            match raw_meter["commodity"]:
                case "elektriciteit":
                    commodity = "electra"
                case _:
                    commodity = raw_meter["commodity"]

            meter_obj = MeterCreateDTO(
                name=f'{raw_meter["name"]}_on_{raw_meter["street"]}',
                commodity=commodity,
                status=raw_meter["status"],
                ean=raw_meter["ean"],
                source_id=str(raw_meter["id"]),
                installed_at=datetime.fromisoformat(raw_meter["created_at"]),
            )
            meter_objects.append(meter_obj)

        return meter_objects

    def format_measurements(self, raw_channels) -> list[ChannelWithMeasurements]:
        if len(raw_channels) < 0:
            log.critical("No measurements found on source")
            return []

        channel_names: list[str] = [d["channel"] for d in raw_channels]

        measurements_per_channel: list[ChannelWithMeasurements] = []
        count = 0
        for i, channel in enumerate(channel_names):
            measurements: list[MeasurementCreateDTO] = []
            for measurement in raw_channels[i]["values"]:
                measurements.append(
                    MeasurementCreateDTO(
                        value=measurement["value"], timestamp=measurement["timestamp"]
                    )
                )
                count += 1

            measurements_per_channel.append(
                ChannelWithMeasurements(
                    channel_name=channel, measurements=measurements
                )
            )

        log.info("fetched %s measurements", count)

        return measurements_per_channel

    async def fetch_day_measurements(self, source_id: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""

        formatted_day = f"{date.year}/{date.month}/{date.day}"
        raw_measurements = await self.make_request(
            f"{self.base_url}/measurements/{source_id}/types/interval/days/{formatted_day}"
        )

        return self.format_measurements(raw_measurements)

    async def fetch_month_measurements(self, source_id: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""

        formatted_month = f"{date.year}/{date.month}"
        raw_measurements = await self.make_request(
            f"{self.base_url}/measurements/{source_id}/types/interval/months/{formatted_month}"
        )

        return self.format_measurements(raw_measurements)
