"""
This component provides support for a virtual cover.

"""

import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.config_validation import (PLATFORM_SCHEMA)
from homeassistant.components.cover import (
    ATTR_CURRENT_POSITION,
    ATTR_POSITION,
    CoverDeviceClass,
    CoverEntity,
)

# TODO: during state
from homeassistant.const import (
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING,
    Platform,
)
_LOGGER = logging.getLogger(__name__)

CONF_NAME = "name"
CONF_INITIAL_VALUE = "initial_value"
CONF_INITIAL_POSITION = "initial_position"
CONF_INITIAL_AVAILABILITY = "initial_availability"

DEFAULT_INITIAL_VALUE = "open"
DEFAULT_INITIAL_POSITION = 100
DEFAULT_INITIAL_AVAILABILITY = True

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_INITIAL_VALUE, default=DEFAULT_INITIAL_VALUE): cv.string,
    vol.Optional(CONF_INITIAL_POSITION, default=DEFAULT_INITIAL_POSITION): cv.positive_int,
    vol.Optional(CONF_INITIAL_AVAILABILITY, default=DEFAULT_INITIAL_AVAILABILITY): cv.boolean,
})


async def async_setup_platform(_hass, config, async_add_entities, _discovery_info=None):
    locks = [VirtualCover(config)]
    async_add_entities(locks, True)


class VirtualCover(CoverEntity):
    """Representation of a Virtual cover."""

    def __init__(self, config):
        """Initialize the Virtual cover device."""
        self._name = config.get(CONF_NAME)

        # Are we adding the domain or not?
        self.no_domain_ = self._name.startswith("!")
        if self.no_domain_:
            self._name = self.name[1:]
        self._unique_id = self._name.lower().replace(' ', '_')

        self._state = config.get(CONF_INITIAL_VALUE)
        self._position = config.get(CONF_INITIAL_POSITION)

        self._available = config.get(CONF_INITIAL_AVAILABILITY)
        _LOGGER.info('VirtualCover: {} created'.format(self._name))


    @property
    def is_closed(self):
        """Return if the cover is closed."""
        return self._state == 'closed'

    @property
    def is_open(self):
        """Return if the cover is open."""
        return self._state == 'open'

    def close_cover(self):
        """Close the cover."""
        self.set_cover_position(0)

    def open_cover(self):
        """Open the cover."""
        self.set_cover_position(100)

    def set_cover_position(self, position: int = 0, **kwargs):
        """Move the roller shutter to a specific position."""
        if position <= 0:
            self._position = 0
            self._state = 'closed'
        else:
            self._state = 'open'
            self._position = position


    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    def set_available(self, value):
        self._available = value
        self.async_schedule_update_ha_state()

    @property
    def extra_state_attributes(self):
        """Return the device state attributes."""
        attrs = {
            'friendly_name': self._name,
            'unique_id': self._unique_id,
        }
        return attrs
