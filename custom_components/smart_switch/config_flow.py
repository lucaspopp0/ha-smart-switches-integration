"""Config flow for the Smart Switches integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def _async_has_devices(hass: HomeAssistant) -> bool:
    """Return if there are devices that can be discovered."""
    # Get discovered devices from the Bluetooth integration
    try:
        discovered_devices = bluetooth.async_discovered_service_info(hass)
        
        # Check if any device has "Smart Switch" in its name
        for device_info in discovered_devices:
            if device_info.name and "Smart Switch" in device_info.name:
                return True
                
    except Exception as err:
        _LOGGER.debug("Error checking for Smart Switch devices: %s", err)
        return False
    
    return False


class SmartSwitchConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Switches."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._discovered_devices: dict[str, BluetoothServiceInfoBleak] = {}

    async def async_step_bluetooth(
        self, discovery_info: BluetoothServiceInfoBleak
    ) -> ConfigFlowResult:
        """Handle the bluetooth discovery step."""
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        # Only proceed if the device name contains "Smart Switch"
        if not discovery_info.name or "Smart Switch" not in discovery_info.name:
            return self.async_abort(reason="not_smart_switch")

        self.context["title_placeholders"] = {
            "name": discovery_info.name or discovery_info.address
        }

        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Confirm discovery."""
        if user_input is not None:
            return self.async_create_entry(
                title=self.context["title_placeholders"]["name"],
                data={},
            )

        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders=self.context["title_placeholders"],
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Manual setup - scan for devices
            discovered_devices = bluetooth.async_discovered_service_info(self.hass)
            smart_switches = {}
            
            for device_info in discovered_devices:
                if device_info.name and "Smart Switch" in device_info.name:
                    smart_switches[device_info.address] = device_info
            
            if not smart_switches:
                errors["base"] = "no_devices_found"
            else:
                self._discovered_devices = smart_switches
                return await self.async_step_device_selection()

        return self.async_show_form(
            step_id="user",
            errors=errors,
        )

    async def async_step_device_selection(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle device selection step."""
        if user_input is not None:
            selected_address = user_input["device"]
            selected_device = self._discovered_devices[selected_address]
            
            await self.async_set_unique_id(selected_address)
            self._abort_if_unique_id_configured()
            
            return self.async_create_entry(
                title=selected_device.name or selected_address,
                data={"address": selected_address},
            )

        # Create device list for selection
        device_list = {}
        for address, device_info in self._discovered_devices.items():
            device_list[address] = device_info.name or f"Smart Switch ({address})"

        return self.async_show_form(
            step_id="device_selection",
            data_schema=vol.Schema({
                vol.Required("device"): vol.In(device_list)
            }),
        )


config_entry_flow.register_discovery_flow(DOMAIN, "Smart Switches", _async_has_devices)
