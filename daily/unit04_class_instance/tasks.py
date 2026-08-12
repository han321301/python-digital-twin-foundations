# 클래스 정의 요구사항
# - sensor_id, sensor_type, unit은 필수
# - name은 선택
# - name을 전달하지 않으면 sensor_id를 이름으로 사용
# - 센서마다 독립적인 measurements 리스트를 가짐

class Sensor:
    def __init__(
            self,
            sensor_id: str,
            sensor_type: str,
            unit: str,
            name: str | None = None,
    ):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.measurements = []

        self.name = sensor_id if name is None else name
        # name이 정확히 None인 경우에만 sensor_id가 할당 ("", 0, False와 None을 구분함)
        # self.name = name or sensor_id 
        # ""가 넘어오면 => sensor_id 할당함 (or은 빈문자열을 거짓으로 평가함)

temperature_sensor = Sensor(
    "TEMP-001",
    "temperature",
    "celsius",
    "보일러 온도 센서",
)

vibration_sensor = Sensor(
    "VIB-001",
    "vibration",
    "mm/s",
)

assert temperature_sensor.name == "보일러 온도 센서"
assert vibration_sensor.name == "VIB-001"

assert temperature_sensor.measurements == []
assert vibration_sensor.measurements == []

assert (
    temperature_sensor.measurements
    is not vibration_sensor.measurements
)
