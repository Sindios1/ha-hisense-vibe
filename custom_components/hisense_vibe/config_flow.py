"""Config flow for Hisense Vibe integration."""
from __future__ import annotations

import logging
import json
import ssl
import paho.mqtt.client as mqtt
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CERT_PEM, DEFAULT_USER, DEFAULT_PASS, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

class HisenseVibeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hisense Vibe."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self.host = None
        self.mac = None

    def _trigger_pin(self, host):
        """Connect to TV and trigger the PIN display by sending multiple common trigger commands."""
        try:
            # We use a client ID that is more likely to be accepted (generic but official-looking)
            client = mqtt.Client(client_id="HomeAssistant")
            client.username_pw_set(DEFAULT_USER, DEFAULT_PASS)
            
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            client.tls_set_context(context)
            
            client.connect(host, DEFAULT_PORT, keepalive=60)
            
            # 1. Standard trigger
            client.publish("/remoteapp/tv/ui_service/HomeAssistant/actions/get_pin", "{}")
            
            # 2. Alternative trigger (requesting state often wakes up the PIN logic)
            client.publish("/remoteapp/tv/ui_service/HomeAssistant/actions/gettvstate", "{}")
            
            # 3. Some models need a specific auth type payload
            client.publish("/remoteapp/tv/ui_service/HomeAssistant/actions/get_pin", json.dumps({"auth_type": 1}))
            
            client.disconnect()
            return True
        except Exception as ex:
            _LOGGER.error("Failed to trigger Hisense PIN: %s", ex)
            return False

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            self.host = user_input["host"]
            self.mac = user_input["mac"]
            
            # Try to trigger PIN display on the TV
            if await self.hass.async_add_executor_job(self._trigger_pin, self.host):
                return await self.async_step_pair()
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("mac"): str,
            }),
            errors=errors,
        )

    async def async_step_pair(self, user_input=None) -> FlowResult:
        """Handle the pairing step (PIN entry)."""
        errors = {}
        
        if user_input is not None:
            pin = user_input["pin"]
            
            def _send_pin(host, pin_code):
                try:
                    client = mqtt.Client(client_id="HomeAssistant")
                    client.username_pw_set(DEFAULT_USER, DEFAULT_PASS)
                    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    client.tls_set_context(context)
                    client.connect(host, DEFAULT_PORT)
                    # Use the standard pairing topic
                    client.publish("/remoteapp/tv/ui_service/HomeAssistant/actions/authenticationcode", 
                                   json.dumps({"authNum": pin_code}))
                    client.disconnect()
                    return True
                except Exception:
                    return False

            if await self.hass.async_add_executor_job(_send_pin, self.host, pin):
                return self.async_create_entry(
                    title=f"Hisense TV ({self.host})",
                    data={
                        "host": self.host,
                        "mac": self.mac,
                        "pin": pin,
                    },
                )
            else:
                errors["base"] = "invalid_auth"

        return self.async_show_form(
            step_id="pair",
            data_schema=vol.Schema({
                vol.Required("pin"): vol.All(str, vol.Length(min=4, max=4)),
            }),
            description_placeholders={"host": self.host},
            errors=errors,
        )
