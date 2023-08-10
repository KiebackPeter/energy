from app.energy.provider import EnergyProvider, energy_provider_factory


async def update_with_remote_meters(installation_id: int, name: str, key: str):
    provider = EnergyProvider(
        installation_id,
        energy_provider_factory(name, key),
    )

    meters = await provider.update_meter_list()
    return f"fetched meters: {len(meters)}"


async def update_with_remote_measurements(installation_id: int, name: str, key: str):
    provider = EnergyProvider(
        installation_id,
        energy_provider_factory(name, key),
    )

    meters = await provider.update_meter_list()

    for meter in meters:
        await provider.update_meter_measurements(meter)

    return f"up-to-date meters: {len(meters)}"
