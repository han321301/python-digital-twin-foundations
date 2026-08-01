# ==================================================================
# 최종 구현 과제
# ==================================================================
# 시작 데이터 
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

STATUS_PRIORITY = {
    "unknown": -1,
    "normal": 0,
    "warning": 1,
    "critical": 2,
}

factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "status": "normal",
        "sensors": {
            "TEMP-01": {
                "type": "temperature",
                "status": "normal",
                "measurements": [],
            },
            "VIB-01": {
                "type": "vibration",
                "status": "normal",
                "measurements": [],
            },
        },
    },
}

# ------------------------------------------------------------------
# 1. validate_value(): 측정값 유효성 확인 => bool
def validate_device( value: object) -> bool:
    # bool 타입인지 확인 - 파이썬에서 불 타입은 정수의 하위 클래스라서, 아래 정수인지 확인하는
    # 필터링으로는 불린 타입을 거를 수가 없음
    if isinstance(value, bool):
        return False
    
    # value가 정수 또는 실수가 아니라면 False 
    if not isinstance(value, (int, float)):
        return False 

    # 연쇄 비교 연산자로 -1000 ~ 1000 사이의 값인지 확인 
    return -1000 <= value <= 1000

# 2. classify_status() : 상태 계산 => 상태 문자열 
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

# 3. update_device() : 측정 이력과 상태 갱신 => 성공 여부
def update_device(
        factory: dict,
        device_id: str,
        sensor_id: str,
        value: object,
) -> bool:
    device = factory.get(device_id)

    if device is None:
        return False

    sensors = device.get("sensors", {})
    sensor = sensors.get(sensor_id)

    # [검증] 1. 센서가 없는 경우 처리 
    if sensor is None: 
        return False

    # [검증] 2. 값이 유효하지 않은 경우 처리 
    if not validate_device(value):
        return False

    sensor_type = sensor.get("type")

    # [검증] 3. sensor 타입이 유효하지 않는 경우 처리
    if not isinstance(sensor_type, str):
        return False

    new_status = classify_status(
        sensor_type,
        value,
    )

    if new_status == "unknown":
        return False

    # 모두 통과했으므로 원본 변경 가능 
    # [수정] 1. measurements 
    measurements = sensor.setdefault("measurements", []) # 키의 값을 가져옴, 키가 없다면 새 리스트로 초기화 
    measurements.append(value)

    # [수정] 2. status - 개별 센서의 상태 변경
    sensor["status"] = new_status

    # 모든 센서의 상태만 모은 리스트 생성
    device_statuses = [
        item.get("status", "unknown") # status 값을 가져옴, 없다면 unknown 반환 
        for item in sensors.values() # sensors 딕셔너리의 모든 값을 순회 
    ]

    # 센서의 상태값중 가장 심각한 상태값을 장치의 상태값으로 결정 
    # max(리스트, key=함수) : 리스트에서 값을 하나씩 꺼내 람다함수로 하나씩 넘김 
    # 맥스 함수는 파이썬 내부 임시 변수에 '1등 값'과 '1등 점수'만 덮어쓰기하며 기억하고
    # 순회가 끝나는 순간 최종적으로 남은 값인 1등을 꺼내어 반환한다 
    device["status"] = max(
        device_statuses,
        key = lambda status: STATUS_PRIORITY.get(status, -1)
    )
    return True

# ------------------------------------------------------------------
# 검증 코드 
# ------------------------------------------------------------------
# 1. 정상 측정값 기록 
result = update_device(
    factory,
    "PUMP-01",
    "TEMP-01",
    32.5,
)

assert result is True

assert (
    factory["PUMP-01"]
    ["sensors"]
    ["TEMP-01"]
    ["measurements"]
    == [32.5]
)

assert (
    factory["PUMP-01"]
    ["sensors"]
    ["TEMP-01"]
    ["status"]
    == "warning"
)

assert factory["PUMP-01"]["status"] == "warning"

# 2. 위험 상태 기록 
assert update_device(
    factory,
    "PUMP-01",
    "VIB-01",
    8.5,
) is True

assert (
    factory["PUMP-01"]
    ["sensors"]
    ["VIB-01"]
    ["status"]
    == "critical"
)

assert factory["PUMP-01"]["status"] == "critical"

# 3. 존재하지 않는 장비와 센서
assert update_device(
    factory, "UNKNOWN", "TEMP-01", 25.0
) is False 

# 4. 잘못된 값은 기록하지 않기 
before = repr(factory)

assert update_device(
    factory,
    "PUMP-01",
    "TEMP-01",
    True,
) is False

assert repr(factory) == before
