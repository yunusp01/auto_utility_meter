DOMAIN = "auto_utility_meter"
CONF_SOURCE_SENSOR = "source_sensor"
CONF_INTERVALS = "intervals"
CONF_SENSOR_TYPE = "sensor_type"

SENSOR_TYPE_WATT = "watt"
SENSOR_TYPE_KWH = "kwh"

INTERVAL_OPTIONS = [
    {"value": "hourly", "label": "Stündlich"},
    {"value": "daily", "label": "Täglich"},
    {"value": "weekly", "label": "Wöchentlich"},
    {"value": "monthly", "label": "Monatlich"},
    {"value": "yearly", "label": "Jährlich"},
]

SENSOR_TYPE_OPTIONS = [
    {"value": SENSOR_TYPE_KWH, "label": "Energie-Sensor (kWh)"},
    {"value": SENSOR_TYPE_WATT, "label": "Leistungs-Sensor (Watt)"},
]