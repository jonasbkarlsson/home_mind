"""Constants file"""

from homeassistant.const import __version__ as HA_VERSION

NAME = "Home Mind"
DOMAIN = "home_mind"
VERSION = "0.1.0"
ISSUE_URL = "https://github.com/jonasbkarlsson/home_mind/issues"

# Icons

# Platforms

# Entity keys

# Configuration and options
CONF_ASSIST_SATELLITE_ENTITY = "assist_satellite"
CONF_LAST_RECOGNIZED_FACE_ENTITY = "last_recognized_face"

# Defaults
DEBUG = False
HOLD_OFF_TIME_MINUTES = 120

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
Home Assistant: {HA_VERSION}
-------------------------------------------------------------------
"""
