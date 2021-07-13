import aiohttp
import asyncio
from typing import Any

class TWCManagerClient:
    """TWCManager client."""


    def __init__(self, host: str):
        """Construct a new TWCManager client."""
        self._host = host
    

    async def async_get_config(self) -> dict[str, Any]:
        """Get the current configuration."""
        return await self._async_get(self._host + '/api/getConfig')
    

    async def async_get_policy(self) -> dict[str, Any]:
        """Get the policy configuration."""
        return await self._async_get(self._host + '/api/getPolicy')


    async def async_get_slave_twcs(self) -> dict[str, Any]:
        """Get a list of connected slave TWCs and their state."""
        return await self._async_get(self._host + '/api/getSlaveTWCs')


    async def async_get_status(self) -> dict[str, Any]:
        """Get the current status (charge rate, policy)."""
        return await self._async_get(self._host + '/api/getStatus')
    

    async def _async_get(self,path: str,) -> dict[str, Any]:
        """Get JSON from TWCManager server."""
        async with aiohttp.ClientSession() as session:
            async with session.get(path) as response:
                response.raise_for_status()
                return await response.json()

class Twc:

    def __init__(self, id, data):
        self.id = id
        self.current_vin = data.get('currentVIN')
        self.last_amps_offered = data.get('lastAmpsOffered')
        self.last_heartbeat = data.get('lastHeartbeat')
        self.cars_charging = data.get('carsCharging')
        self.last_vin = data.get('lastVIN')
        self.lifetime_kwh = data.get('lifetimekWh')
        self.max_amps = data.get('maxAmps')
        self.reported_amps_actual = data.get('reportedAmpsActual')
        self.charger_load_in_w = data.get('chargerLoadInW')
        self.state = data.get('state')
        self.version = data.get('version')
        self.volts_phase_a = data.get('voltsPhaseA')
        self.volts_phase_b = data.get('voltsPhaseB')
        self.volts_phase_c = data.get('voltsPhaseC')
        self.last_battery_soc = data.get('lastBatterySOC')
        self.last_charge_limit = data.get('lastChargeLimit')
        self.last_at_home = data.get('lastAtHome')
        self.last_time_to_full_charge = data.get('lastTimeToFullCharge')


async def main():

    url = 'http://192.168.1.4:8080'

    client = TWCManagerClient(url)
    result = await client.async_get_slave_twcs()

    for key, value in result.items():
        if (key != 'total'):
            twc = Twc(key, value)
            print(twc.id)
            print(twc.version)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())