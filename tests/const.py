"""Constants for home_mind tests."""

from homeassistant.const import CONF_API_KEY

from custom_components.home_mind.home_mind.const import (
    CONF_ASSIST_SATELLITE_ENTITY,
    CONF_LAST_RECOGNIZED_FACE_ENTITY,
)

# Mock config data to be used across multiple tests
MOCK_CONFIG_ALL = {
    CONF_API_KEY: "1234",
    CONF_ASSIST_SATELLITE_ENTITY: "assist.satellite_any",
    CONF_LAST_RECOGNIZED_FACE_ENTITY: "sensor.last_recognized_face_any",
}
