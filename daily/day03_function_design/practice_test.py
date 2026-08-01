from practice import *

# 
assert classify_sensor_status(
    "temperature",
    29.9,
) == "normal"

assert classify_sensor_status(
    "temperature",
    30.0,
) == "warning"

assert classify_sensor_status(
    "temperature",
    40.0,
) == "critical"

assert classify_sensor_status(
    "vibration",
    6.2,
) == "warning"