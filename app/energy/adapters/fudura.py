"""Implementation for fudura.nl"""

from .base_adapter import (
    BaseAdapter,
    datetime,
    # log,
    ChannelWithMeasurements,
    MeterCreateDTO,
    # MeasurementCreateDTO,
)



class FuduraAdapter(BaseAdapter):
    """A concrete implemetation working with the Kenter API"""

    def __init__(self, provider_key: str) -> None:
        self.set_access_token()
        self.base_url = "https://fdr-ws-prd.azurewebsites.net/api/v1"

    def set_access_token(self):
        # super().__init__({"x-api-key": provider_key})

        files = {
            "grant_type": (None, "client_credentials"),
            "resource": (
                None,
                "https://fdrwsadprd.onmicrosoft.com/FuduraWebserviceProduction",
            ),
            "client_id": (None, "client_id"),
            "client_secret": (None, "pi_key"),
        }
        post(self.base_url, files)
        return

    async def fetch_meter_list(self) -> list[MeterCreateDTO]:
        """Returns all available meters from endpoint in meter objects"""
        return

    def format_measurements(
        self, raw_measurements: list[dict[str, Any]]
    ) -> list[ChannelWithMeasurements]:
        return

    async def fetch_day_measurements(self, meter: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""
        return self.format_measurements()

    async def fetch_month_measurements(self, meter: str, date: datetime):
        """Get measurement values from a meter on a speficic day"""
        return self.format_measurements()
