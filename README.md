# WhatsMiner Control

[![Active installations](https://img.shields.io/badge/Active-1+-blue?style=for-the-badge)]()
[![GitHub issues](https://img.shields.io/github/issues/k3nshiDev/Whatsminer-Control?style=for-the-badge)](https://github.com/k3nshiDev/Whatsminer-Control/issues)
[![Version - 1.0.0](https://img.shields.io/badge/Version-1.0.0-009688?style=for-the-badge)](https://github.com/k3nshiDev/Whatsminer-Control/releases/tag/v1.0.0)
[![HACS Badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

**NOT Official Home Assistant integration for monitoring and controlling WhatsMiner devices.**  
Opens the official WhatsMiner API for Home Assistant users.

---

## Requirements

- Minimum Home Assistant version: `2024.12`  
- WhatsMiner device connected to the same network (IP + port required, default port 4433)

---

## Features

This integration allows you to:

- Monitor the working status of your WhatsMiner devices  
- Track real-time hashrate, power consumption, fan speed, chip temperature, and board temperatures  
- View miner uptime and device type  
- Add custom names to each miner in Home Assistant  
- Poll the miner status automatically every 30 seconds using a **DataUpdateCoordinator**  
- Integrate with HACS for easy installation and updates  

---

## Supported Sensors

The following entities are created automatically for each miner:

| Sensor | Unit | Description |
|--------|------|-------------|
| hash-realtime | TH/s | Current miner hashrate |
| power-realtime | W | Current power consumption |
| chip-temp-min | °C | Minimum chip temperature |
| chip-temp-avg | °C | Average chip temperature |
| chip-temp-max | °C | Maximum chip temperature |
| power-limit | W | Configured power limit |
| fan-speed-in | RPM | Fan speed intake |
| fan-speed-out | RPM | Fan speed exhaust |
| bootup-time | s | Miner uptime |
| environment-temperature | °C | Device ambient temperature |
| board-temperature | °C | Temperatures of individual hash boards |

Additionally, a **binary sensor** reports whether the miner is working.

---

## Installation

### HACS

1. Add the repository in HACS → Integrations → **Custom Repositories**  
   - URL: `https://github.com/k3nshiDev/Whatsminer-Control`  
   - Category: Integration  
2. Install the integration and select **Release v1.0.0**  
3. Restart Home Assistant

### Manual

1. Download the latest release from [GitHub](https://github.com/k3nshiDev/Whatsminer-Control/releases/latest)  
2. Copy the folder `whatsminer_control` into `config/custom_components/`  
3. Restart Home Assistant

---

## Configuration

1. Add a new integration in Home Assistant → **WhatsMiner Control**  
2. Enter the miner **IP address** and **port** (default 4433)  
3. Optionally, provide a **custom name** for easy identification  

---

## Device Info

Each miner entity exposes device information including:

- Device type (e.g., M30S+_VH20)  
- Manufacturer: `MicroBT`  
- IP address and configuration URL

---

## Contributing

Feel free to submit **issues** or **pull requests** if you want to help improve the integration.  

