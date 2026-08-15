measurements = [
    {
        "sensor_id": "TEMP-01",
        "value": 28.4,
        "timestamp": "10:03",
    },
    {
        "sensor_id": "VIB-01",
        "value": 4.2,
        "timestamp": "10:01",
    },
    {
        "sensor_id": "TEMP-01",
        "value": 31.7,
        "timestamp": "10:05",
    },
    {
        "sensor_id": "VIB-01",
        "value": 6.8,
        "timestamp": "10:04",
    },
    {
        "sensor_id": "TEMP-01",
        "value": 29.1,
        "timestamp": "10:02",
    },
]

# ------------------------------------------------------------------
# 1. 센서별 그룹화
# ------------------------------------------------------------------
def group_by_sensor(
        measurements: list[dict],
) -> dict[str, list[dict]]:
    grouped = {}

    for m in measurements:
        sensor_id = m["sensor_id"]

        grouped.setdefault(sensor_id, []).append(m)

    return grouped

# 검증
grouped = group_by_sensor(measurements)
print("grouped :", grouped)
assert len(grouped["TEMP-01"]) == 3
assert len(grouped["VIB-01"]) == 2

# ------------------------------------------------------------------
# 2. 센서별 최신 상태값 반환
# ------------------------------------------------------------------
def build_latest_state(
    measurements: list[dict],
) -> dict[str, dict]:
    """
    원본 measurements를 수정하지 않는다.
    측정값이 없으면 {}를 반환한다.
    """
    latest = {}

    for m in measurements:
        sensor_id = m["sensor_id"]

        if sensor_id not in latest:
            latest[sensor_id] = m
            continue

        if m["timestamp"] > latest[sensor_id]["timestamp"]:
            latest[sensor_id] = m
    return latest

# 검증
latest = build_latest_state(measurements)

assert latest["TEMP-01"]["value"] == 31.7
assert latest["TEMP-01"]["timestamp"] == "10:05"

assert latest["VIB-01"]["value"] == 6.8
assert latest["VIB-01"]["timestamp"] == "10:04"

assert build_latest_state([]) == {}