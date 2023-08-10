from datetime import datetime
from typing import Any

from app.core.logger import log
from app.energy.providers.base_provider import BaseProvider
from app.database.schemas.measurements import MeasurementCreateDTO
from app.database.schemas.meter import MeterCreateDTO, MeterInBD


class TumsAdapter(BaseProvider):
    """A concrete implemetation working with the Kenter API"""

    def __init__(self, api_key) -> None:
        super().__init__({"Authorization": "Basic " + api_key})
