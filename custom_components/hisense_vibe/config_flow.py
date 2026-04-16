"""Config flow for Hisense Vibe integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HisenseVibeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hisense Vibe."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.host = None
        self.mac = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            self.host = user_input[\"host\"]
            self.mac = user_input[\"mac\"]
            
            # Move to pairing step
            return await self.async_step_pair()

        return self.async_show_form(
            step_id=\"user\",
            data_schema=vol.Schema({
                vol.Required(\"host\"): str,
                vol.Required(\"mac\"): str,
            }),
            errors=errors,
        )

    async def async_step_pair(self, user_input=None) -> FlowResult:
        """Handle the pairing step (PIN entry)."""
        errors = {}
        
        # In a real scenario, we would trigger the PIN on TV here via MQTT
        # For this version, we assume the user triggers it or it's already visible
        
        if user_input is not None:
            pin = user_input[\"pin\"]
            # Here we would send the PIN via MQTT to authenticate
            # For now, we'll finish the flow and assume success
            
            return self.async_create_entry(
                title=f\"Hisense TV ({self.host})\",
                data={
                    \"host\": self.host,
                    \"mac\": self.mac,
                    \"pin\": pin,
                },
            )

        return self.async_show_form(
            step_id=\"pair\",
            data_schema=vol.Schema({
                vol.Required(\"pin\"): str,
            }),
            description_placeholders={\"host\": self.host},
            errors=errors,
        )
