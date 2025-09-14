"""General helpers"""

# pylint: disable=relative-beyond-top-level
import logging
from typing import Any
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)


class Validator:
    """Validator"""

    @staticmethod
    def is_float(element: Any) -> bool:
        """Check that argument is a float"""
        try:
            float(element)
            return True
        except ValueError:
            return False
        except TypeError:
            return False


def get_parameter(config_entry: ConfigEntry, parameter: str, default_val: Any = None):
    """Get parameter from OptionsFlow or ConfigFlow"""
    if parameter in config_entry.options.keys():
        return config_entry.options.get(parameter)
    if parameter in config_entry.data.keys():
        return config_entry.data.get(parameter)
    return default_val


def get_subentry_parameter(config_entry: ConfigEntry, subentry_type: str, parameter: str, default_val: Any = None):
    """Get parameter from OptionsFlow or ConfigFlow"""
    conversation_subentry = next(
        (
            sub
            for sub in config_entry.subentries.values()
            if sub.subentry_type == subentry_type
        ),
        None,
    )
    if not conversation_subentry:
        return default_val

    if parameter in conversation_subentry.data.keys():
        return conversation_subentry.data.get(parameter)
    return default_val
