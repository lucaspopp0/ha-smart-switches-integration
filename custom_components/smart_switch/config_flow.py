"""Config flow for the Smart Switches integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.data_entry_flow import AbortFlow
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from homeassistant.components import bluetooth

from collections import OrderedDict

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

def format_unique_id(address: str) -> str:
    """Format the UUId of a smart switch from its Bluetooth MAC address"""
    return address.replace(":", "").lower()

class SmartSwitchConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Switches."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.id = DOMAIN
        self.discovered_info: bluetooth.BluetoothServiceInfoBleak | None = None
        self.discovered_infos: dict[str, bluetooth.BluetoothServiceInfoBleak] = {}

    async def _async_set_device(self, discovery_info: bluetooth.BluetoothServiceInfoBleak) -> None:
        """Set the device to work with"""
        self.discovered_info = discovery_info
        await self.async_set_unique_id(
            format_unique_id(discovery_info.address),
            raise_on_progress=False,
        )
        self._abort_if_unique_id_configured()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the user step for picking discovered devices"""
        if user_input is not None:
            discovery_info = self.discovered_infos[user_input['address']]
            await self._async_set_device(discovery_info)
            return await self._async_create_entry_from_discovery(user_input)

        await self._async_discover_devices()
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required('address'): vol.In(
                        {
                            address: discovery_info.name
                            for address, discovery_info in self.discovered_infos.items()
                        }
                    )
                }
            )
        )
    
    async def _async_discover_devices(self) -> None:
        scanner = bluetooth.async_get_scanner(self.hass)
        await scanner.discover(timeout=5)

        current_addresses = self._async_current_ids(include_ignore=False)
        for connectable in (True, False):
            for discovery_info in bluetooth.async_discovered_service_info(self.hass, connectable):
                # Ignore all devices without "Smart Switch" in the name
                if discovery_info.name.find("Smart Switch") == -1:
                    continue

                address = discovery_info.address
                if (
                    format_unique_id(address) in current_addresses
                    or address in self.discovered_infos.keys()
                ):
                    continue

                print(discovery_info)

                if discovery_info.connectable:
                    self.discovered_infos[address] = discovery_info

        if not self.discovered_infos:
            raise AbortFlow("no_devices_found")
        
    async def async_step_bluetooth(
            self, discovery_info: bluetooth.BluetoothServiceInfoBleak,
    ) -> ConfigFlowResult:
        """Bluetooth discovery step"""
        _LOGGER.debug("Discovered bluetooth device: %s", discovery_info.as_dict())
        await self._async_set_device(discovery_info)
        return await self.async_step_confirm()

    async def async_step_confirm(
            self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirms a single device"""
        assert self.discovered_info is not None
        if user_input is not None:
            return await self._async_create_entry_from_discovery(user_input)
            
        self._set_confirm_only()
        return self.async_show_form(
            step_id="confirm",
            data_schema=vol.Schema({}),
            description_placeholders={
                "name": self.discovered_info.name,
            }
        )

    async def _async_create_entry_from_discovery(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Create an entry from a discovery"""
        assert self.discovered_info is not None
        return self.async_create_entry(
            title=self.discovered_info.name,
            data=self.discovered_info,
        )
    
