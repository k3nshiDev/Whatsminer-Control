"""Sensor platform for WhatsMiner Control."""

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = {
    "hash-realtime": {
        "name": "Hashrate Realtime",
        "unit": "TH/s",
        "icon": "mdi:speedometer",
    },
    "power-realtime": {
        "name": "Power",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
    },
    "chip-temp-min": {
        "name": "Chip Temperature Min",
        "unit": "°C",
        "icon": "mdi:thermometer-low",
        "device_class": "temperature",
    },
    "chip-temp-avg": {
        "name": "Chip Temperature Avg",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "chip-temp-max": {
        "name": "Chip Temperature Max",
        "unit": "°C",
        "icon": "mdi:thermometer-high",
        "device_class": "temperature",
    },
    "power-limit": {
        "name": "Power Limit",
        "unit": "W",
        "icon": "mdi:flash",
        "device_class": "power",
    },
    "fan-speed-in": {
        "name": "Fan Speed In",
        "unit": "RPM",
        "icon": "mdi:fan",
    },
    "fan-speed-out": {
        "name": "Fan Speed Out",
        "unit": "RPM",
        "icon": "mdi:fan",
    },
    "bootup-time": {
        "name": "Uptime",
        "unit": "s",
        "icon": "mdi:clock-outline",
    },
    "environment-temperature": {
        "name": "Environment Temperature",
        "unit": "°C",
        "icon": "mdi:thermometer",
        "device_class": "temperature",
    },
    "up-freq-finish": {
        "name": "Up-Freq Finish",
        "icon": "mdi:hammer-wrench",  # небольшая правка: корректная иконка mdi
    },
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Entry function for sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SensorEntity] = []
    for key, meta in SENSORS.items():
        entities.append(WhatsMinerSensor(coordinator, entry, key, meta))

    boards = (
        coordinator.data.get("msg", {}).get("summary", {}).get("board-temperature", [])
    )

    entities = [
        WhatsMinerSensor(coordinator, entry, key, meta) for key, meta in SENSORS.items()
    ]

    boards = (
        coordinator.data.get("msg", {}).get("summary", {}).get("board-temperature", [])
    )
    entities.extend(
        WhatsMinerBoardTempSensor(coordinator, entry, idx) for idx in range(len(boards))
    )

    async_add_entities(entities)


class WhatsMinerSensor(CoordinatorEntity, SensorEntity):
    """Generic WhatsMiner sensor."""

    def __init__(self, coordinator, entry, key, meta) -> None:
        """Init function for sensors."""
        super().__init__(coordinator)

        self._entry = entry
        self._key = key

        self._attr_name = f"{entry.title} {meta['name']}"
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = meta.get("unit")
        self._attr_icon = meta.get("icon")
        self._attr_device_class = meta.get("device_class")

    @property
    def native_value(self):
        """Return sensor value from coordinator."""
        return self.coordinator.data.get("msg", {}).get("summary", {}).get(self._key)

    @property
    def device_info(self) -> DeviceInfo:
        """Device info function for sensors."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            manufacturer="MicroBT",
            model=self.coordinator.api.get_device_type(),
            configuration_url=f"http://{self._entry.data['host']}",
        )


class WhatsMinerBoardTempSensor(CoordinatorEntity, SensorEntity):
    """Temperature sensor for a single hash board."""

    _attr_device_class = "temperature"
    _attr_native_unit_of_measurement = "°C"
    _attr_icon = "mdi:chip"

    def __init__(self, coordinator, entry, board_index: int) -> None:
        """Init function for sensors."""
        super().__init__(coordinator)

        self._entry = entry
        self._board_index = board_index

        self._attr_name = f"{entry.title} Board {board_index + 1} Temperature"
        self._attr_unique_id = f"{entry.entry_id}_board_{board_index}_temp"

    @property
    def native_value(self):
        """Return board temperature, if available."""
        boards = (
            self.coordinator.data.get("msg", {})
            .get("summary", {})
            .get("board-temperature", [])
        )
        if self._board_index < len(boards):
            return boards[self._board_index]
        return None

    @property
    def device_info(self):
        """Device info function for sensors."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name=self._entry.title,
            manufacturer="MicroBT",
            model=self.coordinator.api.get_device_type(),
            configuration_url=f"http://{self._entry.data['host']}",
        )
