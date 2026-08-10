# ==================================================================
# unit 5 반복문과 컴프리헨션
# ==================================================================
# 여러 데이터를 순회하면서 선택·변환·집계하는 방법을 구분
# 언제 일반 반복문과 컴프리헨션·any()·all()을 써야 하는지 판단

measurements = [
    {"sensor_id": "TEMP-01", "type": "temperature", "value": 28.4},
    {"sensor_id": "TEMP-02", "type": "temperature", "value": 34.2},
    {"sensor_id": "VIB-01", "type": "vibration", "value": 4.1},
    {"sensor_id": "VIB-02", "type": "vibration", "value": 8.5},
    {"sensor_id": "TEMP-03", "type": "temperature", "value": 41.0},
]
# ------------------------------------------------------------------
# 1. 반복한다는 것은 무엇인가
# ------------------------------------------------------------------
values = [28.4, 34.2, 41.0]

for value in values:
    print(value)

values = [
    {"value": 10},
    {"value": 20},
]

for item in values: # item은 딕셔너리 객체 자체의 참조(주소)를 가져옴
    item["value"] += 1

print(values) #[{'value': 11}, {'value': 21}]

values = [10,20]

for value in values: # 리스트 요소의 값이 할당됨 
    value += 1 # 참조값이 아니라 할당된 값을 수정함 

print(values) #[10, 20]


# ------------------------------------------------------------------
# 2. 측정값에 상태 붙이기
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

def classify_status(
        sensor_type: str,
        value: float,
) -> str:
    threshold = THRESHOLDS[sensor_type]

    if value > threshold["critical"]:
        return "critical"

    if value > threshold["warning"]:
        return "warning"

    return "normal"

# 첫번째 방법 - 덮어쓰기(원본변경)
for measurement in measurements:
    measurement["status"] = classify_status(measurement["type"], measurement["value"])

# 두번째 방법 - 새로운 데이터 생성
processed = []

for measurement in measurements:
    new_measurement = {
        **measurement,
        "status": classify_status(measurement["type"], measurement["value"])
    }
    processed.append(new_measurement)

print(processed[0]) # {'sensor_id': 'TEMP-01', 'type': 'temperature', 'value': 28.4, 'status': 'normal'}

# 실습 
def process_measurements(
        measurements: list[dict],
) -> list[dict]:
    """
    원본 measurements를 변경하지 않는다.
    각 항목에 status를 추가한다.
    새로운 리스트를 반환한다.
    """
    new_measurements = []
    for measurement in measurements:
        updated = {
            **measurement, 
            "status": classify_status(measurement["type"], measurement["value"])
        }
        new_measurements.append(updated)
    return new_measurements


source = [
    {
        "sensor_id": "TEMP-01",
        "type": "temperature",
        "value": 35.0,
    }
]

result = process_measurements(source)
print(result)
assert source[0].get("status") is None # 원본에는 status가 없다 
assert result[0]["status"] == "warning" # status는 warning이다 
assert result is not source 
assert result[0] is not source[0]


# ------------------------------------------------------------------
# 3. 반복문의 세 가지 대표 작업
# ------------------------------------------------------------------
# 1) 변환: 측정 값 -> 상태가 포함된 측정값
# 2) 필터링: 전체 센서 -> 비정상 센서
# 3) 집계: 측정 값 여러개 -> 평균 


# ------------------------------------------------------------------
# 4. 필터링 - 비정상 센서 찾기
# ------------------------------------------------------------------
processed = [
    {
        "sensor_id": "TEMP-01",
        "value": 28.4,
        "status": "normal",
    },
    {
        "sensor_id": "TEMP-02",
        "value": 34.2,
        "status": "warning",
    },
    {
        "sensor_id": "VIB-02",
        "value": 8.5,
        "status": "critical",
    },
]

# normal이 아닌 센서만 추출하기
abnormal = []

for measurement in processed:
    if measurement["status"] != "normal":
        abnormal.append(measurement)

# 리스트 컴프리헨션
abnormal = [measurement for measurement in processed
            if measurement["status"] != "normal"]

# id만 반환하는 메서드
def find_abnormal_sensors(measurements: list[dict]) -> list[str]:
    abnormal = []
    for measurement in measurements:
        if measurement["status"] != "normal":
            abnormal.append(measurement["sensor_id"])
    return abnormal

assert find_abnormal_sensors(processed) == ['TEMP-02', 'VIB-02']

# ------------------------------------------------------------------
# 5. continue는 언제 필요한가: 중첩문과 가드절(guard clause/early exit)의 가독성
# ------------------------------------------------------------------
measurements = [
    {
        "sensor_id": "TEMP-01",
        "value": 25,
        "active": True,
    },
    {
        "sensor_id": "TEMP-02",
        "value": 999,
        "active": False,
    },
    {
        "sensor_id": "TEMP-03",
        "value": 30,
        "active": True,
    },
]

total = 0 
count = 0

# 중첩 구조
for measurement in measurements:
    if measurement["active"]:
        if measurement["value"] is not None:
            if measurement["value"] >= 0:
                ...

# 중첩 구조를 줄이는 가드 형태 
for measurement in measurements:
    if not measurement["active"]:
        continue

    if measurement["value"] is None:
        continue

    if measurement["value"] < 0:
        continue
    ...



# ------------------------------------------------------------------
# 6. 평균 계산 - 집계 이해하기
# ------------------------------------------------------------------
total = 0
for measurement in measurements:
    total += measurement["value"]

average = total / len(measurements)
print(average)

# 빈리스트가 들어온다면 ZeroDivisionError 발생 

# 
def calculate_average(measurements: list[dict]) -> float | None:
    """
    측정값이 하나 이상이면 평균 반환
    없으면 None
    sum() 사용 가능
    """
    if not measurements:
        return None

    total = 0
    for measurement in measurements:
        total += measurement["value"]

    return total / len(measurements)

values = [
    {"value": 10},
    {"value": 20},
    {"value": 30},
]

assert calculate_average(values) == 20.0
assert calculate_average([]) is None

# ------------------------------------------------------------------
# 7. 7. 상태별 개수 집계
# ------------------------------------------------------------------
processed = [
    {"status": "normal"},
    {"status": "warning"},
    {"status": "normal"},
    {"status": "critical"},
    {"status": "warning"},
]

def summarize_status_counts(measurements: list[dict]) -> dict[str, int]:
    # 초기값
    counts = {
        "normal": 0,
        "warning": 0,
        "critical": 0,
    }

    for measurement in measurements:
        status = measurement["status"]
        counts[status] += 1
    return counts

result = summarize_status_counts(processed)
print(result)

# ------------------------------------------------------------------
# 8. any() — 하나라도 위험한가?
# ------------------------------------------------------------------




# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------



# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------
