"""Implementation for tums.nl"""

from .base_adapter import (
    BaseAdapter,
    # datetime,
    # log,
    # ChannelWithMeasurements,
    # MeterCreateDTO,
    # MeasurementCreateDTO,
)



class TumsAdapter(BaseAdapter):
    """A concrete implemetation working with the Kenter API"""

    def __init__(self, api_key) -> None:
        super().__init__({"Authorization": "Basic " + api_key})
