from datetime import datetime, timedelta
from random import random, randint, choice
from app.energy.providers.base_provider import BaseProvider
from app.database.schemas.channel import ChannelWithMeasurements
from app.database.schemas.measurements import MeasurementCreateDTO
from app.database.schemas.meter import MeterCreateDTO


class MockAdapter(BaseProvider):
    """A mock adapter for testing Energyprovider"""

    def __init__(self, provider_key: str) -> None:
        pass

    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        """Mock | Double a number of create_meter objects"""

        meter_objects: list[MeterCreateDTO] = []
        for _ in range(6):
            meter_obj = MeterCreateDTO(
                name=choice(
                    ["hoofdmeter", "geen hoofdmeter", "tussenmeter", "dynamische meter"]
                ),
                commodity=choice(["electra", "eletrischiteit", "water", "gas"]),
                status=choice(
                    [
                        "GOOD",
                        "GOOD",
                        "-",
                        "MISSING DATA",
                        "GOOD",
                    ]
                ),
                ean=str(randint(199999999, 999999999)),
                source_id=str(randint(199999999, 999999999)),
                installed_at=datetime.today(),
            )
            meter_objects.append(meter_obj)

        return meter_objects

    def mock_measurements(self, days: int, date: datetime):
        """Mock | Double a number of create_measurements objects"""

        date = date - timedelta(days=days)
        measurements_per_channel: list[ChannelWithMeasurements] = []

        for i in range(2):
            measurements_per_channel[i].channel_name = choice(
                ["DELIVERY", "BACKDELIVERY", "MOCKDELIVERY", "DOEDELIVERY"]
            )
            measurements_per_channel[i].measurements = [
                MeasurementCreateDTO(value=random(), timestamp=date.timestamp() + 900)
                for _ in range(90 * days)
            ]
        return measurements_per_channel

    async def fetch_day_measurements(
        self, source_id: str, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Get measurement values from a meter on a speficic day"""
        return self.mock_measurements(1, date)

    async def fetch_month_measurements(
        self, source_id: str, date: datetime
    ) -> list[ChannelWithMeasurements]:
        """Get measurement values from a meter on a speficic day"""
        return self.mock_measurements(30, date)
