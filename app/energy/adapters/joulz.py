"""Implementation for joulz.nl"""

from typing import Any
from .base_adapter import (
    BaseAdapter,
    datetime,
    # timedelta,
    log,
    ChannelWithMeasurements,
    MeterCreateDTO,
    # MeasurementCreateDTO,
)


class JoulzAdapter(BaseAdapter):
    """A concrete implemetation working with the Joulz API"""

    def __init__(self, provider_key: str) -> None:
        super().__init__()
        self.key = provider_key
        self.surfix = f"/?apikey={self.key}&format=json"  # NOTE maybe add '?tf=utc'
        self.base_url = "https://joulz.e-dataportal.nl/api/v3"

    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        """Returns all available meters from endpoint in meter objects"""

        raw_meter_list = await self.make_request(
            self.base_url + "/connections" + self.surfix
        )
        meter_objects: list[MeterCreateDTO] = []
        for raw_meter in raw_meter_list["values"]:
            # print(raw_meter)
            if raw_meter["contracted_power_kw"]:
                commodity = "electricity"
            if raw_meter["contracted_power_m3"]:
                commodity = "gas"
            else:
                commodity = "unknown"

            # TODO check which meter/channels are available
            if len(raw_meter["measurement-points"]) > 1:
                # print(raw_meter["measurement-points"])
                pass

            meter_obj = MeterCreateDTO(
                name=f'{raw_meter["description"]}_on_{raw_meter["address"]}_from_{raw_meter["company"]["name"]}',
                commodity=commodity,
                status="",
                ean=f'{raw_meter["measurement-points"][0]["ean"]}:{raw_meter["measurement-points"][0]["subcode"]}',
                source_id=str(raw_meter["id"]),
                installed_at=datetime.fromisoformat(raw_meter["first-measurement"]),
            )
            meter_objects.append(meter_obj)

        return meter_objects

    def format_measurements(
        self, raw_measurements: list[dict[str, Any]]
    ) -> list[ChannelWithMeasurements]:
        if len(raw_measurements) < 0:
            log.critical("No measurements found on source")
            return []
        #     channels: list[str] = [d["channel"] for d in raw_measurements]
        #     measurements_per_channel: dict[str, list[MeasurementCreateDTO]] = {}
        #     count = 0

        #     for i, channel in enumerate(channels):
        #         measurements: list[MeasurementCreateDTO] = []

        #         for measurement in raw_measurements[i]["values"]:
        #             measurement_obj = MeasurementCreateDTO(
        #                 value=measurement["value"],
        #                 timestamp=datetime.utcfromtimestamp(measurement["timestamp"])
        #             )
        #             measurements.append(measurement_obj)
        #             count += 1
        #         measurements_per_channel[channel] = measurements

        #     log.info("fetched %s measurements", count)

        return measurements_per_channel

    async def fetch_day_measurements(self, source_id: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""

        # day_before = date - timedelta(days=1)
        # formatted_day_before = f"/{day_before.year}/{day_before.month}/{day_before.day}"
        # formatted_day = f"/{date.year}/{date.month}/{date.day}"

        raw_measurements = await self.make_request(
            self.base_url
            + f"/aggregates/?per=daily&dap={source_id}&begin={formatted_day_before}&end={formatted_day}"
            + self.surfix
        )
        # print(raw_measurements)
        return self.format_measurements(raw_measurements)

    async def fetch_month_measurements(self, source_id: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""

        if date.month < 12:
            day_before = datetime(date.year, date.month, date.day + 1)
        else:
            day_before = datetime(date.year + 1, 1, date.day + 1)

        # formatted_day_before = f"/{day_before.year}/{day_before.month}/{day_before.day}"
        # formatted_day = f"/{date.year}/{date.month}/{date.day}"

        raw_measurements = await self.make_request(
            self.base_url
            + f"/aggregates/?per=daily&dap={source_id}&begin={formatted_day_before}&end={formatted_day}"
            + self.surfix
        )
        # print(raw_measurements)
        return self.format_measurements(raw_measurements)
