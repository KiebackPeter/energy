# import pytest
# from datetime import datetime
# from fastapi import HTTPException

# from app.energy.provider import EnergyProvider
# from app.energy.adapters.energiemissie import EnergiemissieAdapter
# from app.schemas.meter import MeterCreateDTO, MeterInBD
# from app.schemas.measurements import MeasurementCreateDTO


# class TestEnergyProvider:
#     # Tests that EnergyProvider initializes correctly
#     def test_initialization(self):
#         energy_provider = EnergyProvider('energiemissie', 'source_key')
#         assert energy_provider._source_provider == 'energiemissie'
#         assert energy_provider._source_key == 'source_key'
#         assert isinstance(energy_provider.provider, EnergiemissieAdapter)

#     # Tests that give_adapter() returns the correct adapter for a valid provider
#     def test_give_adapter_valid_provider(self):
#         energy_provider = EnergyProvider('energiemissie', 'source_key')
#         assert isinstance(energy_provider.give_adapter(), EnergiemissieAdapter)

#     # Tests that get_meter_list() returns a list of MeterCreateDTO objects
#     @pytest.mark.asyncio
#     async def test_get_meter_list(self):
#         energy_provider = EnergyProvider('energiemissie', 'source_key')
#         meter_list = await energy_provider.get_meter_list()
#         assert isinstance(meter_list, list)
#         assert all(isinstance(meter, MeterCreateDTO) for meter in meter_list)

#     # Tests that get_day_measurements() returns a dictionary of MeasurementCreateDTO objects
#     @pytest.mark.asyncio
#     async def test_get_day_measurements(self):
#         energy_provider = EnergyProvider('energiemissie', 'source_key')
#         meter = MeterInBD(source_id=123)
#         date = datetime.now()
#         day_measurements = await energy_provider.fetch_day_measurements(meter, date)
#         assert isinstance(day_measurements, dict)
#         assert all(isinstance(measurement, MeasurementCreateDTO) for measurement in day_measurements.values())

#     # Tests that get_month_measurements() returns a dictionary of MeasurementCreateDTO objects
#     @pytest.mark.asyncio
#     async def test_get_month_measurements(self):
#         energy_provider = EnergyProvider('energiemissie', 'source_key')
#         meter = MeterInBD(source_id=123)
        
#         date = datetime.now()
#         month_measurements = await energy_provider.get_month_measurements(meter, date)
#         assert isinstance(month_measurements, dict)
#         assert all(isinstance(measurement, MeasurementCreateDTO) for measurement in month_measurements.values())

#     # Tests that give_adapter() raises an exception for an invalid provider
#     def test_give_adapter_invalid_provider(self):
#         with pytest.raises(HTTPException):
#             energy_provider = EnergyProvider('invalid_provider', 'source_key')
#             energy_provider.give_adapter()