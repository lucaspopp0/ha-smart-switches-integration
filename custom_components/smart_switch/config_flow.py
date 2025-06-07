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

    async def async_step_only_step(self, user_input):
        fields: OrderedDict[vol.Marker, Any] = OrderedDict()

        return self.async_show_form(
            step_id="only_step",
            data_schema=vol.Schema(fields),
            errors={},
            last_step=True,
        )

    def is_matching(self, other_flow: SmartSwitchConfigFlow) -> bool:
        """Return True if other_flow is matching this flow."""
        return self.id == DOMAIN
