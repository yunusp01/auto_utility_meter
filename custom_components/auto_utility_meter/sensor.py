import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.utility_meter.sensor import UtilityMeterSensor
from homeassistant.components.integration.sensor import IntegrationSensor
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import translation
from homeassistant.components.utility_meter.const import DATA_UTILITY, DATA_TARIFF_SENSORS

from .const import (
    DOMAIN, 
    CONF_SOURCE_SENSOR, 
    CONF_INTERVALS, 
    CONF_SENSOR_TYPE, 
    SENSOR_TYPE_WATT
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup der Sensoren (Integral und Utility Meter)."""
    
    config = {**entry.data, **entry.options}
    source_entity_id = config.get(CONF_SOURCE_SENSOR)
    intervals = config.get(CONF_INTERVALS, [])
    sensor_type = config.get(CONF_SENSOR_TYPE)

    ent_reg = er.async_get(hass)
    dev_reg = dr.async_get(hass)
    source_entry = ent_reg.async_get(source_entity_id)
    
    device_info = None
    device_name = "Sensor"
    
    if source_entry and source_entry.device_id:
        device_entry = dev_reg.async_get(source_entry.device_id)
        if device_entry:
            device_info = {"identifiers": device_entry.identifiers}
            device_name = device_entry.name_by_user or device_entry.name

    clean_base = device_name.replace(" Energy", "").replace(" energy", "").replace(" Energie", "").replace(" energie", "").replace(" Power", "").replace(" power", "")
    
    translations = await translation.async_get_translations(hass, hass.config.language, "entity", {DOMAIN})
    actual_source = source_entity_id

    # --- SCHRITT 1: WATT -> KWH UMRECHNUNG ---
    if sensor_type == SENSOR_TYPE_WATT:
        integral_unique_id = f"{entry.entry_id}_total_energy"
        integral_obj_id = f"{clean_base.lower().replace(' ', '_')}_total_energy"
        
        total_name_suffix = translations.get(f"component.{DOMAIN}.entity.sensor.total_energy.name", "Total Energy")
        total_full_name = f"{clean_base} {total_name_suffix}"
        
        energy_integral_sensor = IntegrationSensor(
            hass=hass,
            source_entity=source_entity_id,
            name=total_full_name,
            round_digits=3, # Hohe interne Präzision
            unit_prefix="k",
            unit_time="h",
            integration_method="left",
            unique_id=integral_unique_id,
            max_sub_interval=timedelta(seconds=20)
        )
        
        energy_integral_sensor.entity_id = f"sensor.{integral_obj_id}"
        energy_integral_sensor._attr_device_info = device_info
        energy_integral_sensor._attr_native_unit_of_measurement = "kWh"
        energy_integral_sensor._attr_device_class = "energy"
        energy_integral_sensor._attr_state_class = "total_increasing"
        
        async_add_entities([energy_integral_sensor])
        actual_source = energy_integral_sensor.entity_id

    # --- SCHRITT 2: UTILITY METER ERSTELLEN ---
    entities = []
    for interval in intervals:
        unique_id = f"{entry.entry_id}_{interval}"
        obj_id = f"{clean_base.lower().replace(' ', '_')}_{interval}_energy"
        
        lang_key = f"component.{DOMAIN}.entity.sensor.{interval}.name"
        suffix = translations.get(lang_key, interval.capitalize())
        full_name = f"{clean_base} {suffix}"

        entities.append(
            AutoUtilityMeterSensor(
                hass=hass,
                source_entity=actual_source,
                name=full_name,
                interval=interval,
                unique_id=unique_id,
                device_info=device_info,
                object_id=obj_id
            )
        )

    async_add_entities(entities)

class AutoUtilityMeterSensor(UtilityMeterSensor):
    """Spezialisierter Utility Meter Sensor."""
    _attr_has_entity_name = False 

    def __init__(self, hass, source_entity, name, interval, unique_id, device_info, object_id):
        self.entity_id = f"sensor.{object_id}"
        self._attr_unique_id = unique_id
        self._attr_name = name
        self._attr_translation_key = interval 

        super().__init__(
            hass=hass,
            source_entity=source_entity,
            name=name,
            meter_type=interval,
            meter_offset=timedelta(0),
            net_consumption=False,
            unique_id=unique_id,
            cron_pattern=None,
            delta_values=False,
            parent_meter=None,
            periodically_resetting=True,
            tariff_entity=None,
            tariff=None,
            sensor_always_available=False
        )
        self._attr_device_info = device_info
        self._parent_meter = unique_id

    @property
    def name(self) -> str:
        return self._attr_name

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        attrs = super().extra_state_attributes or {}
        attrs["friendly_name"] = self._attr_name
        return attrs

    async def async_added_to_hass(self):
        if DATA_UTILITY not in self.hass.data:
            self.hass.data[DATA_UTILITY] = {}
        
        self.hass.data[DATA_UTILITY][self._parent_meter] = {
            DATA_TARIFF_SENSORS: [self]
        }
        await super().async_added_to_hass()