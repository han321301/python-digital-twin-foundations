# ==================================================================
# unit 12 - Python 객체를 API용 JSON 데이터로 바꾸기
# ==================================================================
# Python 내부 객체
# → JSON으로 표현 가능한 형태
# → API 요청/응답

# ------------------------------------------------------------------
# 1. json.dumps()로 파이썬 객체를 json형식 문자열로 변환하기 
# ------------------------------------------------------------------
from datetime import datetime

device = {
    "device_id": "PUMP-01",
    "status": "warning",
    "latest_value": 35.2,
    "updated_at": datetime.now(),
}

import json

# json.dumps() 파이썬 객체 -> json 형식의 문자열로 변환
# json.dumps(device)
# TypeError: Object of type datetime is not JSON serializable

# ------------------------------------------------------------------
# 2. JSON이 이해하는 타입은?
# ------------------------------------------------------------------
# str, int, float, bool, None, list, dict
# 반면 datetime은 문자열로 바꿔줘야함 
# : datetime.now().isoformat()

device = {
    "device_id": "PUMP-01",
    "status": "warning",
    "latest_value": 35.2,
    "updated_at": datetime.now().isoformat()
}

jsonStr = json.dumps(device)
print(jsonStr)

# ------------------------------------------------------------------
# 3. 함수로 변환하기
# ------------------------------------------------------------------
def device_to_dict(device: dict) -> dict:
    return {
        "device_id": device["device_id"],
        "status": device["status"],
        "latest_value": device["latest_value"],
        "updated_at": device["updated_at"].isoformat(),
    }

device = {
    "device_id": "PUMP-01",
    "status": "warning",
    "latest_value": 35.2,
    "updated_at": datetime.now(),
}

payload = device_to_dict(device)

print(payload)

# ------------------------------------------------------------------
# 4. 반대 방향 구현: json str -> python 객체 
# ------------------------------------------------------------------
payload = {
    "device_id": "PUMP-01",
    "value": 35.2,
    "timestamp": "2026-08-26T17:30:00",
}

def measurement_from_dict(payload: dict) -> dict:
    return {
        "device_id": payload["device_id"],
        "value": float(payload["value"]),
        "timestamp": datetime.fromisoformat(payload["timestamp"]),
    }

measurement = measurement_from_dict(payload)

print(measurement)
print(type(measurement["timestamp"])) #<class 'datetime.datetime'>

# ------------------------------------------------------------------
# 5. API 데이터 검증 우선하기 
# ------------------------------------------------------------------
payload = {
    "device_id": "",
    "value": "abc",
    "timestamp": "yesterday",
}

def measurement_from_dict(payload: dict) -> dict:
    device_id = payload["device_id"]

    if not device_id: # Falsy(None, "", 0, [], {}, (), False)
        raise ValueError("device_id가 비어있습니다.")

    value = float(payload["value"])
    timestamp = datetime.fromisoformat(payload["timestamp"])

    return {
        "device_id": device_id,
        "value": value,
        "timestamp": timestamp,
    }

# ------------------------------------------------------------------
# 6. 중첩 데이터 변환 (리스트컴프리헨션 활용)
# ------------------------------------------------------------------
device = {
    "device_id": "PUMP-01",
    "status": "warning",
    "sensors": [
        {
            "sensor_id": "TEMP-01",
            "value": 35.2,
            "updated_at": datetime.now(),
        },
        {
            "sensor_id": "VIB-01",
            "value": 4.8,
            "updated_at": datetime.now(),
        },
    ],
}

def device_to_dict(device: dict) -> dict:
    return {
        "device_id": "PUMP-01",
        "status": "warning",
        "sensors": [
            {
                "sensor_id": sensor["sensor_id"],
                "value": sensor["value"],
                "updated_at": sensor["updated_at"].isoformat(),
            }
            for sensor in device["sensors"]
        ],
    }
