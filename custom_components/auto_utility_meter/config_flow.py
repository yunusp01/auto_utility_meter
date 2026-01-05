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
    SENSOR_TYPE_WATT,
    SENSOR_TYPE_GAS,
    SENSOR_TYPE_WATER,
    SENSOR_TYPE_OPTIONS
)

# Erlaubte Einheiten für die Validierung
VALID_UNITS = {
    SENSOR_TYPE_WATT: ["W", "kW"],
    SENSOR_TYPE_KWH: ["Wh", "kWh", "MWh"],
    SENSOR_TYPE_GAS: ["m³", "m3", "ft³"],
    SENSOR_TYPE_WATER: ["L", "m³", "m3", "gal"]
}

class AutoUtilityMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Setup-Flow für die Ersteinrichtung."""
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # Validierung der Einheit
            source_entity_id = user_input[CONF_SOURCE_SENSOR]
            sensor_type = user_input[CONF_SENSOR_TYPE]
            
            state = self.hass.states.get(source_entity_id)
            if state:
                unit = state.attributes.get("unit_of_measurement", "")
                if sensor_type in VALID_UNITS and unit not in VALID_UNITS[sensor_type]:
                    errors["base"] = "wrong_unit"
                else:
                    return self.async_create_entry(title=user_input[CONF_SOURCE_SENSOR], data=user_input)
            else:
                errors["base"] = "sensor_not_found"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_SENSOR_TYPE, default=SENSOR_TYPE_KWH): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=SENSOR_TYPE_OPTIONS,
                        mode=selector.SelectSelectorMode.DROPDOWN
                    )
                ),
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
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return AutoUtilityMeterOptionsFlowHandler(config_entry)

class AutoUtilityMeterOptionsFlowHandler(config_entries.OptionsFlow):
    """Verwaltet das Zahnrad-Menü (Optionen)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # Gleiche Validierung wie im Haupt-Flow
            source_entity_id = user_input[CONF_SOURCE_SENSOR]
            sensor_type = user_input[CONF_SENSOR_TYPE]
            
            state = self.hass.states.get(source_entity_id)
            if state:
                unit = state.attributes.get("unit_of_measurement", "")
                if sensor_type in VALID_UNITS and unit not in VALID_UNITS[sensor_type]:
                    errors["base"] = "wrong_unit"
                else:
                    return self.async_create_entry(title="", data=user_input)
            else:
                errors["base"] = "sensor_not_found"

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
            }),
            errors=errors
        )
