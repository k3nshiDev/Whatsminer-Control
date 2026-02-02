"""WhatsMiner Control integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .api import WhatsMinerAPI
from .const import DOMAIN
from .coordinator import WhatsMinerCoordinator

PLATFORMS = ["binary_sensor", "sensor"]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WhatsMiner Control from a config entry."""

    api = WhatsMinerAPI(
        host=entry.data["host"],
        port=entry.data["port"],
    )

    coordinator = WhatsMinerCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
