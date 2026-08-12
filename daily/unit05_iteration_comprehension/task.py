# ------------------------------------------------------------------
# 통합 과제
# ------------------------------------------------------------------
measurements = [
    {
        "sensor_id": "TEMP-01",
        "type": "temperature",
        "value": 28.4,
        "active": True,
    },
    {
        "sensor_id": "TEMP-02",
        "type": "temperature",
        "value": 34.2,
        "active": True,
    },
    {
        "sensor_id": "VIB-01",
        "type": "vibration",
        "value": 4.1,
        "active": False,
    },
    {
        "sensor_id": "VIB-02",
        "type": "vibration",
        "value": 8.5,
        "active": True,
    },
    {
        "sensor_id": "TEMP-03",
        "type": "temperature",
        "value": 41.0,
        "active": True,
    },
]

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

# 1. 활성 센서라면 상태값을 붙여 반환. 비활성인 경우 스킵하고 원본은 수정하지 않음 
def process_active_measurements(
        measurements: list[dict],
) -> list[dict]:
    updated_measurements = []

    # 비활성 상태 제외
    for measurement in measurements:
        if not measurement["active"]:
            continue
        # measurement.get("active", False) - active키가 없는 경우에 발생하는 에러 방지 필요한 경우 

        # 센서 타입 구분 -> 한계치와 비교하여 상태 판정
        value = measurement["value"]
        threshold = THRESHOLDS[measurement["type"]]

        if value > threshold["critical"]:           
            status =  "critical"

        elif value > threshold["warning"]:
            status = "warning"
        else:
            status = "normal"
        
        updated_measurements.append({
                        **measurement, 
                        "status": status,
                    })

    return updated_measurements

updated_measurements = process_active_measurements(measurements)
print(updated_measurements)


# 2. critical 상태인 센서만 반환하기 
def find_critical_sensor_ids(
        measurements: list[dict],
) -> list[str]:
    return [
        measurement["sensor_id"] # 가져올 거 
        for measurement in measurements # 대상 데이터 
        if measurement["status"] == "critical" # 조건 
    ]

    # critical_sensorsIdx = []
    # for measurement in measurements:
    #     if measurement.get("status", None) == "critical":
    #         critical_sensorsIdx.append(measurement["sensor_id"])

    # return critical_sensorsIdx

result = find_critical_sensor_ids(updated_measurements)
print(result)

# 3. 평균값 
def calculate_average_value(
        measurements: list[dict]
) -> float | None:
    if not measurements:
        return None

    total = sum(
        measurement["value"]
        for measurement in measurements
    )

    return total / len(measurements)


result = calculate_average_value(updated_measurements)
print(result)

# 4. 상태별 개수
def summarize_status_counts(
    measurements: list[dict],
) -> dict[str, int]:
    counts = {
        "normal": 0,
        "warning": 0,
        "critical": 0,
    }

    for measurement in measurements:
        counts[measurement["status"]] += 1

    return counts

result = summarize_status_counts(updated_measurements)
print(result)

# 5. 설비 최종 상태 출력
# critical 센서가 하나라도 있음
# → critical

# critical은 없고 warning이 하나라도 있음
# → warning

# 모두 normal
# → normal

# 측정값 자체가 없음
# → unknown

def determine_device_status(
    measurements: list[dict],
) -> str:
    if not measurements:
        return "unknown"
    
    # any() 하나라도 있으면 True 뱉는 걸 활용 
    if any(
        measurement["status"] == "critical"
        for measurement in measurements
    ):
        return "critical"

    if any(
        measurement["status"] == "warning"
        for measurement in measurements
    ):
        return "warning"

    return "normal"

