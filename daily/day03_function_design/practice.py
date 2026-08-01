
# ==================================================================
# day03 function_design
# ==================================================================
# 2일차 코드 
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "location": "ROOM-A",
        "status": "normal",
        "sensors": {
            "TEMP-01": {
                "type": "temperature",
                "unit": "celsius",
                "measurements": [],
            },
        },
    },
}

# 오늘 추가할 기능 
# 1. 측정값 추가
# 2. 센서 상태 판정
# 3. 장비 전체 상태 갱신


# ------------------------------------------------------------------
# 1. 함수의 입력과 반환값 
# ------------------------------------------------------------------
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

def classify_sensor_status(
        sensor_type: str,
        value: float,
) -> str:
    # 임계값 가져오기
    limits = THRESHOLDS[sensor_type]

    if value >= limits["critical"]:
        return "critical"
    elif value >= limits["warning"]:
        return "warning"
    return "normal"

# [+] 데이터에서 차이점과 공통점 구분하기 
#   : 센서타입이 달라도 내부 속성("warning", "critical")은 같음 -> 공통 규칙으로 취급


# ------------------------------------------------------------------
# 2. 원본 변경과 새 객체 반환
# ------------------------------------------------------------------
sensor = {
    "type": "temperature",
    "measurements": [],
}

# 1. 원본 변경 방식
# 리스크: 상태 변화 추적 어려움, 부작용 발생 가능
def add_measurement(
        sensor: dict,
        value: float,
) -> None:
    sensor["measurements"].append(value)


result = add_measurement(sensor, 32.5)

print(sensor) # {'type': 'temperature', 'measurements': [32.5]}

# 2. 새 객체 반환 방식
# 리스크 - 복사 비용이 발생, 깊은 복사 비쌈, 코드가 길다
original = {
    "type": "temperature",
    "measurements": [],
}
from copy import deepcopy
def create_updated_sensor(sensor: dict, value: float) -> dict:
    updated_sensor = deepcopy(sensor)
    updated_sensor["measurements"].append(value)

    return updated_sensor

updated = create_updated_sensor(original, 32.5)

print(original["measurements"]) # []
print(updated["measurements"]) # [32.5]


# ------------------------------------------------------------------
# 3. 함수는 한 가지 책임만 맡는다 
# ------------------------------------------------------------------
# 책임을 분리하여 함수를 생성 -> 조합 함수로 순서대로 호출 
# 조합 함수
# def record_measurement(...) -> bool:
    # 센서 조회
    # → 값 검증
    # → 측정값 추가
    # → 센서 상태 변경
    # → 장비 상태 변경

# ------------------------------------------------------------------
# 4. 위치 인자와 키워드 인자
# ------------------------------------------------------------------

# 키워드 인자를 지정하여 호출문 명확성 높이기
# '*' 뒤에 인자는 이름을 적어 호출해야한다
def register_sensor(
        factory: dict,
        device_id: str,
        sensor_id: str,
        *,
        sensor_type: str,
        unit: str,
        activated: bool,
    ) -> bool:
    ...


register_sensor(
    factory,
    "PUMP-01",
    "TEMP-01",
    sensor_type = "temperature", # 이런식으로 이름 안적으는다면 타입에러남
    unit = "celsius",
    activated=True, # 특히 불리언 값의 경우 유용하다 
)

# ------------------------------------------------------------------
# 5. 타입 힌트가 보장하는 것 
# ------------------------------------------------------------------
# 타입 힌트는 강제되는 것이 아니라서 다른 타입을 넘겨도 에러가 안난다. 
def classify_sensor_status(
        sensor_type: str,
        value: float,
) -> str:
    ...

classify_sensor_status("sensor-01", "10") # 에러나지 않음 

Senosor = dict[str]
Sensor = {"value": 10} # 이것도 에러 안남


# ------------------------------------------------------------------
# 6. *args **kwargs => 불명확한 인자 정의 
# ------------------------------------------------------------------
# *args : 여러 측정 값을 받을 수 있다
# **kwargs : 타입명시 없이 여러 값을 받을 수 있다
def create_sensor(
    sensor_id: str,
    **metadata,
) -> dict:
    return {
        "sensor_id": sensor_id,
        "metadata": metadata,
    }

create_sensor(
    "TEMP-01",
    location="ROOM-A",
    maker="ABC",
    anything="허용됨",
)
