"""Support for Hisense TV media player."""
from __future__ import annotations

import json
import logging
import ssl
import tempfile
import os
import paho.mqtt.client as mqtt
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.components import wake_on_lan
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CERT_PEM, DEFAULT_USER, DEFAULT_PASS, DEFAULT_PORT, SOURCES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Hisense TV platform."""
    async_add_entities([HisenseVibeEntity(entry)], True)

class HisenseVibeEntity(MediaPlayerEntity):
    """Representation of a Hisense TV."""

    def __init__(self, entry: ConfigEntry) -> None:
        """Initialize the TV entity."""
        self._entry = entry
        self._host = entry.data[\"host\"]
        self._mac = entry.data[\"mac\"]
        self._pin = entry.data[\"pin\"]
        self._name = entry.title
        self._state = MediaPlayerState.OFF
        self._client = None
        self._attr_unique_id = entry.entry_id
        self._attr_name = self._name
        self._attr_supported_features = (
            MediaPlayerEntityFeature.PAUSE
            | MediaPlayerEntityFeature.PLAY
            | MediaPlayerEntityFeature.STOP
            | MediaPlayerEntityFeature.TURN_OFF
            | MediaPlayerEntityFeature.TURN_ON
            | MediaPlayerEntityFeature.VOLUME_MUTE
            | MediaPlayerEntityFeature.VOLUME_STEP
            | MediaPlayerEntityFeature.SELECT_SOURCE
        )
        self._attr_source_list = list(SOURCES.keys())

    def _get_mqtt_client(self):
        """Create and return a configured MQTT client."""
        client = mqtt.Client(client_id=\"HomeAssistantVibe\")
        client.username_pw_set(DEFAULT_USER, DEFAULT_PASS)
        
        # Write cert to temp file for SSL context
        with tempfile.NamedTemporaryFile(delete=False, suffix=\".pem\") as cert_file:
            cert_file.write(CERT_PEM.encode())
            cert_path = cert_file.name

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        # In a real scenario we'd use load_cert_chain if needed
        # context.load_cert_chain(certfile=cert_path)
        
        client.tls_set_context(context)
        os.unlink(cert_path)
        return client

    def send_command(self, topic, payload):
        """Send a command to the TV via MQTT."""
        try:
            client = self._get_mqtt_client()
            client.connect(self._host, DEFAULT_PORT)
            client.publish(topic, json.dumps(payload))
            client.disconnect()
        except Exception as ex:
            _LOGGER.error(\"Failed to send command to Hisense TV: %s\", ex)

    async def async_turn_on(self) -> None:
        """Turn the media player on."""
        wake_on_lan.send_magic_packet(self._mac)
        self._state = MediaPlayerState.ON

    async def async_turn_off(self) -> None:
        """Turn the media player off."""
        self.send_command(\"/remoteapp/tv/ui_service/HomeAssistant/actions/key\", {\"key\": \"KEY_POWER\"})
        self._state = MediaPlayerState.OFF

    async def async_volume_up(self) -> None:
        """Volume up the media player."""
        self.send_command(\"/remoteapp/tv/ui_service/HomeAssistant/actions/key\", {\"key\": \"KEY_VOLUMEUP\"})

    async def async_volume_down(self) -> None:
        """Volume down the media player."""
        self.send_command(\"/remoteapp/tv/ui_service/HomeAssistant/actions/key\", {\"key\": \"KEY_VOLUMEDOWN\"})

    async def async_mute_volume(self, mute: bool) -> None:
        """Mute the volume."""
        self.send_command(\"/remoteapp/tv/ui_service/HomeAssistant/actions/key\", {\"key\": \"KEY_MUTE\"})

    async def async_select_source(self, source: str) -> None:
        """Select input source."""
        if source in SOURCES:
            payload = SOURCES[source]
            self.send_command(\"/remoteapp/tv/ui_service/HomeAssistant/actions/changesource\", payload)

    @property
    def state(self) -> MediaPlayerState:
        """Return the state of the TV."""
        return self._state
