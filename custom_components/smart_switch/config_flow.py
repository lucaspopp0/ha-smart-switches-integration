"""Config flow for the Smart Switches integration."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

async def _async_has_devices(hass: HomeAssistant) -> bool:
    # """Return if there are devices that can be discovered."""
    # # TODO Check if there are any devices that can be discovered in the network.
    # devices = await hass.async_add_executor_job(my_pypi_dependency.discover)
    # return len(devices) > 0
    return False

config_entry_flow.register_discovery_flow(DOMAIN, "Smart Switches", _async_has_devices)
