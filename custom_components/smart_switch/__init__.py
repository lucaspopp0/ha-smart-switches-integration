"""The Smart Switches integration."""

from __future__ import annotations

import logging

from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components import bluetooth
from homeassistant.exceptions import ConfigEntryNotReady

from .coordinator import (SmartSwitchConfigEntry, SmartSwitchDataUpdateCoordinator)
from .const import DOMAIN

_PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: SmartSwitchConfigEntry) -> bool:
    """Set up Smart Switches from a config entry."""

    assert entry.unique_id is not None

    address: str = entry.data['address']

    ble_device = bluetooth.async_ble_device_from_address(
        hass, address.upper(), True,
    )

    if not ble_device:
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="device_not_found_error",
        )

    coordinator = entry.runtime_data = SmartSwitchDataUpdateCoordinator(
        hass,
        _LOGGER,
        ble_device,
        entry.unique_id,
        entry.data.get('name', entry.title),
        True,
    )

    entry.async_on_unload(coordinator.async_start())
    if not await coordinator.async_wait_ready():
        raise ConfigEntryNotReady(
            translation_domain=DOMAIN,
            translation_key="advertising_error"
        )
    
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    await hass.config_entries.async_forward_entry_setups(
        entry, Platform.SENSOR,
    )

async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
