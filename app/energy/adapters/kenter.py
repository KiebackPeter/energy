"""Implementation for kenter.nl"""

from .base_adapter import (
    BaseAdapter,
    datetime,
    log,
    ChannelWithMeasurements,
    MeterCreateDTO,
    MeasurementCreateDTO,
)


# cmljaGFyZC52YW5kZW4uaGFtQHpud3Yubmw6VGlqZGVsaWprMTIz
class KenterAdapter(BaseAdapter):
    """A concrete implemetation working with the Kenter API"""

    def __init__(self, api_key) -> None:
        super().__init__({"Authorization": "Basic " + api_key})
        self.base_url = "https://webapi.meetdata.nl/api/1"

    def check_commodity(self, commodity: str):
        match commodity:
            case "E":
                return "electra"
            case "G":
                return "gas"
            case "W":
                return "water"
            case _:
                return commodity

    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        """Returns all available meters from endpoint in meter objects"""

        raw_meter_list = await self.make_request(self.base_url + "/meters")
        
        meter_objects: list[MeterCreateDTO] = []
        for raw_meter in raw_meter_list:
            commodity = self.check_commodity(
                raw_meter["meteringPoints"][0]["productType"]
            )
            # TODO please clean
            if raw_meter["meteringPoints"][0]["masterData"] != []:
                meter_obj = MeterCreateDTO(
                    name=f'{raw_meter["meteringPoints"][0]["masterData"][0]["bpName"]}_on_{raw_meter["meteringPoints"][0]["masterData"][0]["address"]}',
                    commodity=commodity,
                    status=raw_meter["meteringPoints"][0]["masterData"][0]["status"]
                    or "",
                    ean=f'no_ean_{raw_meter["connectionId"]}:{raw_meter["meteringPoints"][0]["meteringPointId"]}',
                    source_id=f'{raw_meter["connectionId"]}:{raw_meter["meteringPoints"][0]["meteringPointId"]}',
                    installed_at=datetime.fromisoformat(
                        raw_meter["meteringPoints"][0]["masterData"][0][
                            "authorizedFrom"
                        ]
                    ),
                )
            else:  # take second item in list: meteringPoints not sure if its always the last or two items
                meter_obj = MeterCreateDTO(
                    name=f'{raw_meter["meteringPoints"][1]["masterData"][0]["bpName"]}_on_{raw_meter["meteringPoints"][1]["masterData"][0]["address"]}',
                    commodity=commodity,
                    status=raw_meter["meteringPoints"][1]["masterData"][0]["status"]
                    or "",
                    ean=f'no_ean_{raw_meter["connectionId"]}:{raw_meter["meteringPoints"][0]["meteringPointId"]}',
                    source_id=f'{raw_meter["connectionId"]}:{raw_meter["meteringPoints"][1]["meteringPointId"]}',
                    installed_at=datetime.fromisoformat(
                        raw_meter["meteringPoints"][1]["masterData"][0][
                            "authorizedFrom"
                        ]
                    ),
                )
            meter_objects.append(meter_obj)

        return meter_objects

    def format_measurements(self, raw_channels) -> list[ChannelWithMeasurements]:
        if raw_channels == []:
            log.warning("No measurements on source")
            return list()
        if raw_channels == {
            "error": "Permission denied. Not authorized for this EAN for the requested date."
        }:
            log.critical("%s", raw_channels)
            return list()

        measurements_per_channel: list[ChannelWithMeasurements] = []
        count = 0

        for channel_name in raw_channels:
            measurements: list[MeasurementCreateDTO] = []

            for measurement in raw_channels[channel_name]:
                measurements.append(
                    MeasurementCreateDTO(
                        value=float(measurement["value"]),
                        timestamp=float(measurement["timestamp"]),
                    )
                )
                count += 1

            measurements_per_channel.append(
                ChannelWithMeasurements(
                    channel_name=channel_name, measurements=measurements
                )
            )

        log.info("fetched %s measurements", count)

        return measurements_per_channel

    async def fetch_day_measurements(self, source_id: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""

        connection_id, meting_point_id = source_id.split(":")
        raw_measurements = await self.make_request(
            f"{self.base_url}/measurements/{connection_id}/{meting_point_id}/{date.year}/{date.month}/{date.day}"
        )

        return self.format_measurements(raw_measurements)

    async def fetch_month_measurements(self, source_id: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""

        connection_id, meting_point_id = source_id.split(":")
        raw_measurements = await self.make_request(
            f"{self.base_url}/measurements/{connection_id}/{meting_point_id}/{date.year}/{date.month}"
        )

        return self.format_measurements(raw_measurements)
