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
    "PUMP-01",
    "TEMP-01",
    "32.5",
)

# ------------------------------------------------------------------
# 5. except은 어디서 하는가?
# ------------------------------------------------------------------
# raise와 except의 구분
# raise: 의도적으로 에러를 만들어 냄, 마찬가지로 하위코드 실행을 멈추고 에러 전파한다
# except: 발생한 에러를 해결함, 에러를 잡아내는 역할


# 측정값 등록과 처리 실패 매세지 출력까지 다하는 상황
def add_measurement():
    try:
        ...
    except InvalidMeasurementError:
        print("등록 실패")

# 문제는 이 함수가 나중에 API에서도 쓸 수 있다는 점
# POST/measurements 
# 이 상황에서 에러 메세지는 필요하지 않음, 대신 HTTP 400 응답을 보냄

# 이 함수가 직접 에러에 대한 처리를 하는게 아니라, 상황을 전달만 하면 됨
# 호출하는 쪽에서 그 오류내용을 출력할지, 로그로 남길지, API 오류 응답으로 보낼지 결정하게 둠 
# 오류를 발견하는 코드와 대응하는 코드를 분리해야 한다는 것
# 해당 함수가 해결할 수 있는가(범위 내인가)를 기준으로 판단 

# 예시 패턴 1 - 메서드 분리 
# 하위 메서드 - 자기 역할만하고 에러는 위로 던진다
def read_config_file():
    with open("config.json", "r") as f:
        return f.read()

# 상위 메서드 - 에러 핸들링
def initialize_program():
    try: 
        config = read_config_file()
    except FileNotFoundError:
        print(f"")

# ------------------------------------------------------------------
# 6. 반환값 정하기 
# ------------------------------------------------------------------
# return {
#     "device_id": device_id,
#     "sensor_id": sensor_id,
#     "value": value,
# }

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

# 최종 함수 
def add_measurement(
    factory: dict,
    device_id: str,
    sensor_id: str,
    raw_value,
) -> dict:

    # 1. 장치와 센서가 유효한지 확인 
    device = factory.get(device_id)

    if device is None: 
        raise DeviceNotFoundError(f"DeviceNotFoundError: {device_id}")
    
    sensor = device["sensors"].get(sensor_id)

    if sensor is None:
        raise SensorNotFoundError(f"SensorNotFoundError: {sensor_id}")

    # 2. 추가하려는 값이 유효한지 확인 
    # 실수로 변환 가능한가
    try:
        value = float(raw_value)
    # 에러 전환  
    except (ValueError, TypeError) as error:
        raise InvalidMeasurementError(
            f"invalid value: {raw_value}"
        ) from error 

    # 범위 내의 값인가 
    minimum, maximun = VALID_RANGES[sensor["type"]]

    if not minimum <= value <= maximun:
        raise InvalidMeasurementError(
            f"InvalidMeasurementError"
        )

    # 3. 데이터를 리스트에 추가
    sensor["measurements"].append(value)

    # 4. 결과 리턴 
    return {
        "device_id": device_id,
        "sensor_id": sensor_id,
        "value": value,
    }

result = add_measurement(
    factory,
    "PUMP-01",
    "TEMP-01",
    "32.5",
)
print(f"new measurement added: {result}")

# ==================================================================
# 과제 정의 
# ==================================================================
records = [
    {
        "device_id": "PUMP-01",
        "sensor_id": "TEMP-01",
        "value": "32.5",
    },
    {
        "device_id": "PUMP-01",
        "sensor_id": "VIB-01",
        "value": "4.8",
    },
    {
        "device_id": "PUMP-01",
        "sensor_id": "TEMP-99",
        "value": "28.0",
    },
    {
        "device_id": "PUMP-99",
        "sensor_id": "TEMP-01",
        "value": "30.1",
    },
    {
        "device_id": "PUMP-01",
        "sensor_id": "TEMP-01",
        "value": "error",
    },
    {
        "device_id": "PUMP-01",
        "sensor_id": "TEMP-01",
        "value": "29.3",
    },
]

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

# 초기 함수 
def ingest_measurements(
    factory: dict,
    records: list[dict],
) -> dict:
    ...

# 리턴 형식 
{
    "total": 6,
    "success_count": 3,
    "failure_count": 3,
    "successes": [
        {
            "device_id": "PUMP-01",
            "sensor_id": "TEMP-01",
            "value": 32.5,
            "unit": "celsius",
        },
        {
            "device_id": "PUMP-01",
            "sensor_id": "VIB-01",
            "value": 4.8,
            "unit": "mm/s",
        },
        {
            "device_id": "PUMP-01",
            "sensor_id": "TEMP-01",
            "value": 29.3,
            "unit": "celsius",
        },
    ],
    "failures": [
        {
            "record": {
                "device_id": "PUMP-01",
                "sensor_id": "TEMP-99",
                "value": "28.0",
            },
            "error_type": "SensorNotFoundError",
            "message": "...",
        },
        ...
    ],
}

# ------------------------------------------------------------------
# 구현부  
# ------------------------------------------------------------------
# {
#         "device_id": "PUMP-01",
#         "sensor_id": "TEMP-01",
#         "value": "32.5",
#     },

def ingest_measurements(
    factory: dict,
    records: list[dict],
) -> dict:
    """
    factory 딕셔너리에서 해당 센서의 값을 추가하기 
    과정에서 성공/실패/전체 처리를 카운팅
    성공/실패 데이터를 리스트에 담기 
    """
    successes = []
    failures = []

    for record in records:
        try:
            # 1. record에서 필요한 필드 추출
            device = record["device_id"]
            sensor = record["sensor_id"]
            value = record["value"]

            # 2. add_measurement() 호출
            result = add_measurement(factory, device, sensor, value)

            # 3. 성공 결과 저장
            successes.append(result)

        except KeyError as error:
            failures.append({
                "record": record,
                "error_type": "KeyError",
                "message": (f"필수 필드가 없습니다. {error.args[0]}")
            })

        except(
            DeviceNotFoundError,
            SensorNotFoundError,
            InvalidMeasurementError,

        ) as error:
            # 4. 예상 가능한 예외는 실패 목록에 저장
            failures.append({
                "record": record,
                "error_type": type(error).__name__,
                "message": str(error)
            })

    return {
        "total": len(records),
        "success_count": len(successes),
        "failure_count": len(failures),
        "successes": successes,
        "failures": failures,
    }

result = ingest_measurements(factory, records)
print(result["failures"])
