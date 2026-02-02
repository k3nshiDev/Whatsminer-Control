"""Config flow for WhatsMiner Control."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT

from .api import WhatsMinerAPI
from .const import DEFAULT_PORT, DOMAIN


class WhatsminerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for WhatsMiner Control."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Show welcome message only."""
        if user_input is not None:
            return await self.async_step_connection()

        return self.async_show_form(step_id="user")

    async def async_step_connection(self, user_input=None):
        """Handle the connection step."""
        if user_input is not None:
            name = user_input.get("name")
            host = user_input.get("host")
            api = WhatsMinerAPI(host, user_input[CONF_PORT])
            miner_type = await self.hass.async_add_executor_job(api.get_device_type)

            if miner_type:
                title = f"{miner_type} ({host})"
            elif name:
                title = f"{name} ({host})"
            else:
                title = f"WhatsMiner {host}"

            title = f"{name} ({host})" if name else f"Whatsminer {host}"

            return self.async_create_entry(
                title=title,
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Optional("name", default="WhatsMiner"): str,
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            }
        )

        return self.async_show_form(step_id="connection", data_schema=schema)
