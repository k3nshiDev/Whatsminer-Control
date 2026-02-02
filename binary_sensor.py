"""Binary sensor for WhatsMiner working status."""

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the WhatsMiner working binary sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([WhatsMinerWorkingSensor(coordinator, entry)])


class WhatsMinerWorkingSensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a WhatsMiner working state."""

    def __init__(self, coordinator, entry) -> None:
        """Init function for binary sensor."""
        super().__init__(coordinator)
        self._entry = entry

        self._attr_name = f"{entry.title} Working"
        self._attr_unique_id = f"{entry.entry_id}_working"
        self._attr_device_class = "power"

    @property
    def is_on(self) -> bool:
        """Return True if miner is working."""
        working = (
            self.coordinator.data.get("msg", {})
            .get("miner", {})
            .get("working", "false")
        )
        return working.lower() == "true"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information for WhatsMiner."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            manufacturer="MicroBT",
            model="WhatsMiner",
            configuration_url=f"http://{self._entry.data['host']}",
        )
