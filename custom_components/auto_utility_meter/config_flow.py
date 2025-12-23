from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN, 
    CONF_SOURCE_SENSOR, 
    CONF_INTERVALS, 
    INTERVAL_OPTIONS, 
    CONF_SENSOR_TYPE, 
    SENSOR_TYPE_KWH,
    SENSOR_TYPE_OPTIONS
)

class AutoUtilityMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Setup-Flow für die Ersteinrichtung."""
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_SOURCE_SENSOR], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                # Typ-Auswahl ganz oben
                vol.Required(CONF_SENSOR_TYPE, default=SENSOR_TYPE_KWH): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=SENSOR_TYPE_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN
                    )
                ),
                # Quell-Sensor (Domain sensor, device_class wird hier weggelassen um flexibel zu sein)
                vol.Required(CONF_SOURCE_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_INTERVALS, default=["daily"]): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=INTERVAL_OPTIONS,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST
                    )
                ),
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return AutoUtilityMeterOptionsFlowHandler(config_entry)

class AutoUtilityMeterOptionsFlowHandler(config_entries.OptionsFlow):
    """Verwaltet das Zahnrad-Menü."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        pass

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        data = self.config_entry.data

        current_type = options.get(CONF_SENSOR_TYPE, data.get(CONF_SENSOR_TYPE, SENSOR_TYPE_KWH))
        current_source = options.get(CONF_SOURCE_SENSOR, data.get(CONF_SOURCE_SENSOR, ""))
        current_intervals = options.get(CONF_INTERVALS, data.get(CONF_INTERVALS, ["daily"]))

        if not isinstance(current_intervals, list):
            current_intervals = [current_intervals]

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_SENSOR_TYPE, default=current_type): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=SENSOR_TYPE_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN
                    )
                ),
                vol.Required(CONF_SOURCE_SENSOR, default=current_source): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="sensor")
                ),
                vol.Required(CONF_INTERVALS, default=current_intervals): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=INTERVAL_OPTIONS,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST
                    )
                ),
            })
        )