DOMAIN = "auto_utility_meter"
CONF_SOURCE_SENSOR = "source_sensor"
CONF_INTERVALS = "intervals"
CONF_SENSOR_TYPE = "sensor_type"

SENSOR_TYPE_WATT = "watt"
SENSOR_TYPE_KWH = "kwh"
SENSOR_TYPE_GAS = "gas"
SENSOR_TYPE_WATER = "water"

INTERVAL_OPTIONS = [
    {"value": "hourly", "label": "Hourly"},
    {"value": "daily", "label": "Daily"},
    {"value": "weekly", "label": "Weekly"},
    {"value": "monthly", "label": "Monthly"},
    {"value": "yearly", "label": "Yearly"},
]

SENSOR_TYPE_OPTIONS = [
    {"value": SENSOR_TYPE_KWH, "label": "Energy Sensor (kWh)"},
    {"value": SENSOR_TYPE_WATT, "label": "Power Sensor (Watt)"},
    {"value": SENSOR_TYPE_GAS, "label": "Gas Sensor (m³)"},
    {"value": SENSOR_TYPE_WATER, "label": "Water Sensor (L or m³)"},
]
