# 복습
# def classify_status(
#         sensor_type: str, value: float,
# ) -> str:
#     thresholds = THRESHOLDS.get(sensor_type)

#     if thresholds is None:
#         return "unknown"

# def update_device(
#         sensor: dict,
#         value: object,
# ) -> bool:
#     if not validate_value(value):
#         return False

#     status = classify_status(sensor["type"], value)

#     sensor["measurements"].append(value)
#     sensor["status"] = status 

#     return True

# 
THRESHOLDS = {
    "temperature": {
        "warning": 30.0,
        "critical": 40.0,
    },
    "vibration": {
        "warning": 5.0,
        "critical": 8.0,
    },
}

def validate_value(value: object) -> bool:
    if isinstance(value, bool):
        return False

    if not isinstance(value, (int, float)):
        return False

    return -1000 <= value <= 1000

def classify_status(
        sensor_type: str,
        value: float,
) -> str:
    thresholds = THRESHOLDS.get(sensor_type) # temperature, vibration 인지 

    if thresholds is None:
        return "unknown"

    if value >= thresholds["critical"]:
        return "critical"

    if value >= thresholds["warning"]:
        return "warning"

    return "normal"

# ------------------------------------------------------------------
# 1. 딕셔너리 센서의 불편함
# ------------------------------------------------------------------
sensor = {
    "sensor_id": "TEMP-01",
    "sensor_type": "temperature",
    "unit": "celsius",
    "measurements": [],
}
# 딕셔너리 구조의 문제점
# - 데이터와 동작이 떨어져 있음(통합되어 있지 않음)
# - 함수 호출 때마다 센서를 전달해야함
# - 외부 코드가 내부 상태를 마음대로 변경할 수 있음


# ------------------------------------------------------------------
# 2. 클래스로 정의하기 
# ------------------------------------------------------------------
class Sensor:
    def __init__( # 생성자 역할로 인스턴스가 생성될 때 최초 1번만 자동으로 실행됨
            self, 
            sensor_id: str,
            sensor_type: str,
            unit: str,
    ) -> None:
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.measurements = [] # __init__ 에서 선언하면 모든 인스턴스가 공유해버리는 버그가 생김

    def add_measurement(
            self, value: float,
    ) -> bool:
        if not validate_value(value):
            return False

        self.measurements.append(value)
        return True

    def latest_value(self) -> float | None:
        # 측정 이력이 없으면 None 반환
        if not self.measurements:
            return None
        
        # 있다면 마지막 값을 반환
        return self.measurements[-1]

    def current_status(self) -> str:
        latest = self.latest_value()

        # 측정 이력이 없으면 unknown 반환
        if latest is None:
            return "unknown"

        # 최신값을 기준으로 상태 판정 - classify_status()
        return classify_status(self.sensor_type, latest)

# 객체 생성하기
temperature_sensor = Sensor(
    sensor_id = "TEMP-01",
    sensor_type = "temperature",
    unit = "celsius",
)
vibration_sensor = Sensor(
    sensor_id="VIB-01",
    sensor_type="vibration",
    unit="mm/s",
)

# 측정값 추가 함수 호출하기 
temperature_sensor.add_measurement(31.5)
temperature_sensor.add_measurement(29.2)
vibration_sensor.add_measurement(8.5)

print(temperature_sensor.latest_value())
print(temperature_sensor.current_status())

print(vibration_sensor.latest_value())
print(vibration_sensor.current_status())


# ------------------------------------------------------------------
# 3. 클래스 속성은 공유됨(인스턴스마다 만들어지고 관리되는 변수가 아님) 
# ------------------------------------------------------------------
class BrokenSensor:
    measurements = [] # 인스턴스마다 만들어지는게 아니라 클래스에 한번만 만들어지는 변수가 됨

    def __init__(
            self, 
            sensor_id : str, 
            sensor_type: str,
            unit: str,
    ) -> None:
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit


sensor_a = BrokenSensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

sensor_b = BrokenSensor(
    "VIB-01",
    "vibration",
    "mm/s",
)

sensor_a.measurements.append(30.0)

print(sensor_a.measurements) # [30.0]
print(sensor_b.measurements) # [30.0]
