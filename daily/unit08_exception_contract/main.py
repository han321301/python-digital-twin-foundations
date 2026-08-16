# 복습 
# 최신값 max()로 가져오기 
# max(
#     measurements,
#     key=lambda x: x["timestamp"]
# )

# setdefault() : grouped.setdefault(sensor_id, []).append(measurement)

# 정렬 
# 새 리스트 : result = sorted(measurements)
# 원본 수정 : measurements.sort()

# ==================================================================
# unit 8 - 예외 처리와 입력 검증
# ==================================================================
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "sensors": {
            "TEMP-01": {
                "type": "temperature",
                "unit": "celsius",
                "measurements": [],
            }
        },
    }
}

# ------------------------------------------------------------------
# 1. 정상 입력만 처리
# ------------------------------------------------------------------
def add_measurement(
        factory, device_id, sensor_id, raw_value,
): 
    device = factory[device_id]
    sensor = device["sensors"][sensor_id]

    value = float(raw_value) 

    sensor["measurements"].append(value)

add_measurement(
    factory,
    "PUMP-01",
    "TEMP-01",
    "32.5",
)

print(
    factory["PUMP-01"]
    ["sensors"]["TEMP-01"]
    ["measurements"]
)

# 값으로 숫자로 변환 불가능한 문자가 들어온다면? => ValueError 발생 

# ------------------------------------------------------------------
# 2. try-except 와 도메인 에러 정의 
# ------------------------------------------------------------------
# ValueError 대신할 사용자 정의 예외
# 필요성: 에러 이름 자체가 설명서가 됨, 파이썬 자체 에러와 업무(도메인) 에러를 구분할 수 있음
class InvalidMeasurementError(ValueError):
    pass

#
def add_measurement(
        factory, device_id, sensor_id, raw_value,
): 
    device = factory[device_id]
    sensor = device["sensors"][sensor_id]

    try:
        value = float(raw_value) 
    except (ValueError, TypeError) as error:
        raise InvalidMeasurementError(
            f"잘못된 측정값입니다: {raw_value}"
        ) from error

    sensor["measurements"].append(value)

# ------------------------------------------------------------------
# 3. 값은 숫자지만 현실적으로 잘못된 경우
# ------------------------------------------------------------------
# 허용 범위 등록
VALID_RANGES = {
    "temperature": (-50, 200), 
    "vibration": (0, 50),
    "pressure": (0, 500),
}

def add_measurement(
    factory,
    device_id,
    sensor_id,
    raw_value,
):
    device = factory[device_id]
    sensor = device["sensors"][sensor_id]

    try:
        value = float(raw_value)
    except(ValueError, TypeError) as error:
        raise InvalidMeasurementError(
            f"잘못된 측정값입니다: {raw_value}"
        ) from error

    # 허용 범위 내 인지 검증
    sensor_type = sensor["type"]
    minimum, maximun = VALID_RANGES[sensor_type]

    if not minimum <= value <= maximun:
        raise InvalidMeasurementError(
            ...
        )

    sensor["measurements"].append(value)

# ------------------------------------------------------------------
# 4. 장비와 센서가 없는 경우 처리 
# ------------------------------------------------------------------
class DeviceNotFoundError(Exception):
    pass

class SensorNotFoundError(Exception):
    pass

def add_measurement(
    factory,
    device_id,
    sensor_id,
    raw_value,
):
    device = factory.get(device_id) # 없다면 return None 

    if device is None: 
        raise DeviceNotFoundError(
            f"장비를 찾을 수 없음: {device_id}"
        )

    sensor = device["sensors"].get(sensor_id)

    if sensor is None:
        raise SensorNotFoundError(
            f"센서를 찾을 수 없음: {sensor_id}"
        )
    ...


add_measurement(
    factory,
    "PUMP-011",
    "TEMP-01",
    "32.5",
)

# ------------------------------------------------------------------
# 5.
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# 6. 
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------

