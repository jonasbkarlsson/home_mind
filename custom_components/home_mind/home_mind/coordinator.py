"""Coordinator for Home Mind"""

import asyncio
from datetime import datetime, UTC
import logging
from homeassistant.config_entries import (
    ConfigEntry,
)

from homeassistant.core import (
    HomeAssistant,
    Event,
    EventStateChangedData,
)

from homeassistant.helpers.device_registry import EVENT_DEVICE_REGISTRY_UPDATED
from homeassistant.helpers.device_registry import async_get as async_device_registry_get
from homeassistant.helpers.device_registry import DeviceRegistry
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.entity_registry import (
    async_get as async_entity_registry_get,
)
from homeassistant.helpers.entity_registry import (
    EntityRegistry,
    async_entries_for_config_entry,
)
from homeassistant.components.assist_pipeline.pipeline import (
    async_get_pipeline,
    async_get_pipelines,
)

from .const import (
    CONF_ASSIST_SATELLITE_ENTITY,
    CONF_LAST_RECOGNIZED_FACE_ENTITY,
    HOLD_OFF_TIME_MINUTES,
)
from .general import get_subentry_parameter


_LOGGER = logging.getLogger(__name__)

STORAGE_KEY = "home_mind.coordinator"
STORAGE_VERSION = 1


# Global lock
home_mind_coordinator_lock = asyncio.Lock()


class HomemindCoordinator:
    """Coordinator class"""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize."""
        self.hass = hass
        self.config_entry = config_entry
        self.platforms = []
        self.listeners = []

        self.last_recognized_face_entity_id = get_subentry_parameter(
            self.config_entry, "conversation", CONF_LAST_RECOGNIZED_FACE_ENTITY
        )
        self.assist_satellite_entity_id = get_subentry_parameter(
            self.config_entry, "conversation", CONF_ASSIST_SATELLITE_ENTITY
        )
        self.last_time = {}

        # self.data_store = storage.Store(hass, STORAGE_VERSION, STORAGE_KEY)

        # Listen for changes to state change.
        if self.last_recognized_face_entity_id:
            self.listeners.append(
                async_track_state_change_event(
                    hass,
                    [self.last_recognized_face_entity_id, self.assist_satellite_entity_id],
                    self.handle_state_change_event,
                )
            )

        #  Listen for new sentences
        self.listeners.append(
            self.hass.bus.async_listen("home_mind_event", self.handle_new_sentence_event)
        )

        # Listen for changes to the device.
        self.listeners.append(
            hass.bus.async_listen(EVENT_DEVICE_REGISTRY_UPDATED, self.device_updated)
        )

    def unsubscribe_listeners(self):
        """Unsubscribed to listeners"""
        for unsub in self.listeners:
            unsub()

    async def device_updated(self, event: Event):  # pylint: disable=unused-argument
        """Called when device is updated"""
        _LOGGER.debug("HomemindCoordinator.device_updated()")
        if "device_id" in event.data:
            entity_registry: EntityRegistry = async_entity_registry_get(self.hass)
            all_entities = async_entries_for_config_entry(
                entity_registry, self.config_entry.entry_id
            )
            if all_entities:
                device_id = all_entities[0].device_id
                if event.data["device_id"] == device_id:
                    if "changes" in event.data:
                        if "name_by_user" in event.data["changes"]:
                            # If the device name is changed, update the integration name
                            device_registry: DeviceRegistry = async_device_registry_get(
                                self.hass
                            )
                            device = device_registry.async_get(device_id)
                            if device.name_by_user != self.config_entry.title:
                                self.hass.config_entries.async_update_entry(
                                    self.config_entry, title=device.name_by_user
                                )

    async def handle_state_change_event(self, event: Event[EventStateChangedData]):
        """Handle state change event.
        EventStateChangedData is supported from Home Assistant 2024.5.5"""

        _LOGGER.debug("HomemindCoordinator.handle_state_change_event()")

        if event.data["entity_id"] == self.last_recognized_face_entity_id:
            await self.handle_last_recognized_face_change(event)
        elif event.data["entity_id"] == self.assist_satellite_entity_id:
            await self.handle_assist_satellite_change(event)
        else:
            _LOGGER.warning(
                "HomemindCoordinator.handle_state_change_event() Unknown entity_id: %s",
                event.data["entity_id"],
            )

    async def handle_last_recognized_face_change(
        self, event: Event[EventStateChangedData]
    ):
        """Handle last recognized face change event."""

        name = event.data["new_state"].state
        _LOGGER.debug("Face = %s", name)
        if not name:
            return
        if isinstance(name, str) and name.lower() in ["none", "unknown", "unavailable"]:
            return

        current_time_utc = datetime.now(UTC)
        if name in self.last_time:
            last_time = self.last_time[name]
            time_since_last = (current_time_utc - last_time).total_seconds()
            _LOGGER.debug(
                "Time since last conversation with %s: %s seconds", name, time_since_last
            )
            if (current_time_utc - last_time).total_seconds() < 60 * HOLD_OFF_TIME_MINUTES:
                return

        current_time = datetime.now().strftime("%H:%M")
        prompt = (
            f"Give a short message to {name}. Use the name of the"
            f"person you are talking with. Adjust to wording to the time of the day,"
            f" which is {current_time} ."
        )

        response = await self.hass.services.async_call(
            domain="home_mind",
            service="generate_content",
            service_data={
                "prompt": prompt,
                "config_entry": self.config_entry.entry_id,
            },
            blocking=True,
            return_response=True,
        )

        if self.hass.states.get(self.assist_satellite_entity_id).state == "idle":
            _LOGGER.debug(
                "HomemindCoordinator.handle_state_change_event() start conversation"
            )
            await self.hass.services.async_call(
                domain="assist_satellite",
                service="start_conversation",
                service_data={
                    "start_message": response["text"],
                    "preannounce": False,
                },
                target={"entity_id": self.assist_satellite_entity_id},
            )
            self.last_time[name] = current_time_utc

        _LOGGER.debug("HomemindCoordinator.handle_state_change_event() ended")

    async def handle_assist_satellite_change(self, event: Event[EventStateChangedData]):
        """Handle assist satellite entity state change event."""
        _LOGGER.debug("HomemindCoordinator.handle_assist_satellite_change()")
        _LOGGER.debug(
            "HomemindCoordinator.handle_assist_satellite_change() new state: %s",
            event.data["new_state"].state,
        )
        # Being in Idle for a long time, and then change to Listening indicates that
        # the user has started to talk to the assist satellite.
        # User initiated conversation.
        #   Idle (long) -> Listening -> Processing -> Responding  [Repeat]
        # Try to interrupt a user initiated conversation, and start a Home Mind initiated
        # conversation instead.

        # Home Mind initiated conversation.
        #   Idle -> Responding ->
        #   Idle (short) -> Listening -> Processing -> Responding [Repeat]
        if event.data["new_state"].state == "listening":
            if event.data["old_state"].state == "idle":
                time_in_idle = (
                    datetime.now(UTC) - event.data["old_state"].last_changed
                ).total_seconds()
                _LOGGER.debug(
                    "HomemindCoordinator.handle_assist_satellite_change()"
                    " time in idle: %s",
                    time_in_idle,
                )
                if time_in_idle > 10:
                    _LOGGER.debug(
                        "HomemindCoordinator.handle_assist_satellite_change()"
                        " Interrupt user initiated conversation"
                    )

                    pipelines = async_get_pipelines(self.hass)
                    _LOGGER.debug("Pipelines: %s", len(pipelines))
                    pipeline = async_get_pipeline(self.hass)
                    _LOGGER.debug("Preferred Pipeline: %s", "len(pipelines)")

                    # await self.hass.services.async_call(
                    #     domain="assist_satellite",
                    #     service="interrupt_conversation",
                    #     target={"entity_id": self.assist_satellite_entity_id},
                    # )

    async def handle_new_sentence_event(self, event: Event):
        """Handle new sentece event."""

        _LOGGER.debug("HomemindCoordinator.handle_new_sentence_event()")
        _LOGGER.debug("Received home_mind_event text: %s", event.data.get("text"))
