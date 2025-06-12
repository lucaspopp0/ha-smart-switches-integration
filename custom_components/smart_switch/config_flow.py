"""Config flow for the Smart Switches integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_entry_flow

from collections import OrderedDict

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class SmartSwitchConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Smart Switches."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.id = DOMAIN

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Smart Switches", data={})

        return self.async_show_form(step_id="user")
