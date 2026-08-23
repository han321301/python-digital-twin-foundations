# ==================================================================
# 구현 과제 - 설비 모니터링 요약 만들기
# ==================================================================
# 목표 리턴 값 형태 
# {
#     "device_id": "PUMP-01",
#     "name": "냉각수 펌프",
#     "sensor_count": 3,
#     "active_sensor_count": 2,
#     "sensors": {
#         "TEMP-01": {
#             "type": "temperature",
#             "unit": "celsius",
#             "latest_value": 30.8,
#             "measurement_count": 3,
#         },
#         "VIB-01": {
#             "type": "vibration",
#             "unit": "mm/s",
#             "latest_value": 4.1,
#             "measurement_count": 2,
#         },
#     },
# }

from dataclasses import dataclass, field

@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str
    _measurements: list[float] = field(
        default_factory=list,
        repr=False
    )

    @property
    def measurements(self):
        return tuple(self._measurements)

    @property
    def latest_value(self):
        return self._measurements[-1:] or None 
        #[-1:])은 리스트가 비어있어도 에러가 나지 않고 빈 리스트 []를 반환
        # 빈 리스트라면 None을 반환하게 됨 

    @property
    def measurement_count(self):
        return len(self._measurements)
    
    def add_measurement(self, value: float) -> None:
        self._measurements.append(value)


@dataclass
class Device:
    device_id: str
    name: str
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

    def add_sensor(self, sensor: Sensor) -> None:
        self.sensors[sensor.sensor_id] = sensor 

    def build_device_snapshot(device: Device) -> dict:
        sensor_data = {}
        active_sensor_count = 0           

        for key, values in device.sensors.items():
            sensor_data[key] = {
                "type": values.sensor_type,
                "unit": values.unit,
                "latest_value": values.latest_value,
                "measurement_count": values.measurement_count
            }

        if values.measurement_count > 0:
            active_sensor_count += 1

        return {
            "device_id": device.device_id,
            "name": device.name,
            "sensor_count": len(device.sensors),
            "active_sensor_count": active_sensor_count,
            "sensors": sensor_data
        }

# 센서 데이터 
temp_sensor = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

vibration_sensor = Sensor(
    "VIB-01",
    "vibration",
    "mm/s",
)

pressure_sensor = Sensor(
    "PRESS-01",
    "pressure",
    "bar",
)

# 장비, 센서 등록 
device = Device(
    device_id="PUMP-01",
    name="냉각수 펌프",
)
device.add_sensor(temp_sensor)
device.add_sensor(vibration_sensor)
device.add_sensor(pressure_sensor)

# 측정값 등록 
temp_sensor.add_measurement(28.5)
temp_sensor.add_measurement(31.2)
temp_sensor.add_measurement(30.8)

vibration_sensor.add_measurement(3.5)
vibration_sensor.add_measurement(4.1)

print(device.build_device_snapshot())
