"""Data update coordinator for WhatsMiner Control."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class WhatsMinerCoordinator(DataUpdateCoordinator):
    """Coordinator for WhatsMiner API."""

    def __init__(self, hass: HomeAssistant, api) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    async def _async_update_data(self):
        """Fetch data from WhatsMiner."""
        try:
            return await self.hass.async_add_executor_job(self.api.get_status)
        except Exception as err:
            raise UpdateFailed(f"Error communicating with miner: {err}") from err
