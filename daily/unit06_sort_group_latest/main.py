# 복습
# 1. 컴프리헨션
values = [20, 35, 42, 28]

warning_values = [
    value
    for value in values
    if value >= 30
]

# all() / any()
has_cirtical = any(
    value >= 40
    for value in values
)

# 원본 수정 여부 
result = sorted(values) # 수정 되지 않음

# (+) 두 리스트 값을 비교할 때
# 순서와 값이 모두 같아야 하는 경우 : list1 == list2 
# 순서 상관없이 값만 같으면 되는 경우 : set(list1) == set(list2)
# 중복을 유지한 채 값만 비교하는 경우(set은 중복은 없앰) : sorted(list1) == sorted(list2)
# 두 리스트가 같은 객체인지(메모리 주소도 같은지) 검증하려는 경우 : lsit1 is list2


# ==================================================================
# unit 6 — 정렬·그룹화·최신 상태 만들기
# ==================================================================
measurements = [
    {
        "sensor_id": "TEMP-01",
        "value": 28.4,
        "timestamp": "2026-08-15T10:03:00",
    },
    {
        "sensor_id": "VIB-01",
        "value": 4.2,
        "timestamp": "2026-08-15T10:01:00",
    },
    {
        "sensor_id": "TEMP-01",
        "value": 31.7,
        "timestamp": "2026-08-15T10:05:00",
    },
    {
        "sensor_id": "VIB-01",
        "value": 6.8,
        "timestamp": "2026-08-15T10:04:00",
    },
    {
        "sensor_id": "TEMP-01",
        "value": 29.1,
        "timestamp": "2026-08-15T10:02:00",
    },
]

# ------------------------------------------------------------------
# 1. sorted() list.sort() 의 차이
# ------------------------------------------------------------------
# timestamp 기준으로 정렬
# sorted()는 새 리스트를 만듬  
sorted_measurements = sorted(
    measurements,
    key=lambda measurement: measurement["timestamp"] #':' 오른쪽 계산 결과를 리턴함
)

print(measurements == sorted_measurements) # False 

# .sort() : 원본을 수정하고 None 반환
result = measurements.sort(
    key=lambda measurement: measurement["timestamp"]
)

# 원본 보존 함수 만들기
def sort_measurements(measurements: list[dict]) -> list[dict]:
    """
    timestamp 오름차순
    원본 수정하지 않음 
    """
    return sorted(measurements, key=lambda m: m['timestamp'])

# 검증
original_first = measurements[0]

result = sort_measurements(measurements)

assert result[0]["timestamp"] == "2026-08-15T10:01:00"
assert result[-1]["timestamp"] == "2026-08-15T10:05:00"

assert measurements[0] is original_first

# ------------------------------------------------------------------
# 2. 최신값 하나를 찾는데 정말 정렬해야 할까?
# ------------------------------------------------------------------
temp_measurements = [
    item
    for item in measurements
    if item["sensor_id"] == "TEMP-01"
]

# 정렬 후 찾는 방식 
temp_measurements = sorted(
    temp_measurements,
    key=lambda item: item["timestamp"],
)

latest1 = temp_measurements[-1]

# max() 활용하는 방식 
latest2 = max(
    temp_measurements,
    key=lambda m : m["timestamp"]
)

print(latest1 is latest2)

# 함수
def find_latest_measurement(
        measurements: list[dict],
        sensor_id: str,
) -> dict | None:
    target_measurements = [
        m
        for m in measurements
        if m["sensor_id"] == sensor_id
    ]
    return max(
        target_measurements, 
        key=lambda m:m["timestamp"], 
        default=None
    )

result = find_latest_measurement(
    measurements,
    "TEMP-010",
)

print(result)

# ------------------------------------------------------------------
# 3. 각 센서들의 최신값만 담는 딕셔너리
# ------------------------------------------------------------------
latest = {}

for m in measurements:
    sensor_id = m["sensor_id"]

    if sensor_id not in latest:
        latest[sensor_id] = m
        continue

    if m["timestamp"] > latest[sensor_id]["timestamp"]:
        latest[sensor_id] = m
