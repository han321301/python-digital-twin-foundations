records = [
    {
        "device_id": "PUMP-01",
        "sensor_id": "TEMP-01",
        "sensor_type": "temperature",
        "value": "28.5",
    },
    {
        "device_id": "PUMP-01",
        "sensor_id": "VIB-01",
        "sensor_type": "vibration",
        "value": "8.7",
    },
    {
        "device_id": "PUMP-02",
        "sensor_id": "TEMP-02",
        "sensor_type": "temperature",
        "value": "43.2",
    },
    {
        "device_id": "PUMP-02",
        "sensor_id": "VIB-02",
        "sensor_type": "vibration",
        "value": "3.5",
    },
    {
            "device_id": "PUMP-02",
            "sensor_id": "VIB-02",
            "sensor_type": "vibration123",
            "value": "3.5",
        },
]

WARNING_THRESHOLDS = {
    "temperature": 40,
    "vibration": 8,
}

# ==================================================================
# 구현 과제 
# ==================================================================
# 조건을 만족하는 순간(이상 상태) 해당 데이터 yield
# device_id가 주어지면 해당 장비만 대상으로 함 
def stream_device_alerts(
        records, threshold, device_id=None
):
    # 장비 필터 -> float(value) -> 경고 기준 이상인지 확인 -> 맞다면 yield 
    for record in records: 
        if device_id is not None: 
            if record["device_id"] != device_id:
                continue

        value = float(record["value"])
        limit = threshold[record["sensor_type"]]

        if value >= limit:
            yield {
                "device_id": record["device_id"],
                "sensor_id": record["sensor_id"],
                "sensor_type": record["sensor_type"],
                "value": value ,
                "threshold": limit
            }
            

alerts = stream_device_alerts(records, WARNING_THRESHOLDS)

for  alert in alerts:
    print(f"alert: {alert}")