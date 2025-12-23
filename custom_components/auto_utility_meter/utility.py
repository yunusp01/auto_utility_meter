from homeassistant.components.utility_meter.const import (
    CONF_SOURCE,
    CONF_CYCLE,
)
from homeassistant.components.utility_meter import DOMAIN as UM_DOMAIN

async def create_utility_meter(hass, name, source, cycle):
    hass.data.setdefault(UM_DOMAIN, {})

    config = {
        name: {
            CONF_SOURCE: source,
            CONF_CYCLE: cycle,
        }
    }

    await hass.services.async_call(
        UM_DOMAIN,
        "reload",
        blocking=True,
    )
