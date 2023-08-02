from datetime import datetime
from typing import Any

from app.core.logger import log
from app.energy.adapters.adapter import BaseAdapter
from app.schemas.measurements import MeasurementCreateDTO
from app.schemas.meter import MeterCreateDTO, MeterInBD


class TumsAdapter(BaseAdapter):
    """A concrete implemetation working with the Kenter API"""

    def __init__(self, api_key) -> None:
        super().__init__({"Authorization": "Basic " + api_key})
