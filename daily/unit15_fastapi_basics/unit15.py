# ==================================================================
# Unit 15 — FastAPI 기초: 센서 측정 API 만들기
# ==================================================================
# 데이터 
DEVICES = {
    "PUMP-01": {
        "device_id": "PUMP-01",
        "name": "Cooling Pump",
        "status": "normal",
        "measurements": [],
    },
    "PUMP-02": {
        "device_id": "PUMP-02",
        "name": "Supply Pump",
        "status": "normal",
        "measurements": [],
    },
}

# 기존 로직
def classify_temperature(value: float) -> str:
    if value >= 40:
        return "critical"

    if value >= 30:
        return "warning"

    return "normal"

# ------------------------------------------------------------------
# 1. FastAPI 애플리케이션 만들기
# ------------------------------------------------------------------
from fastapi import FastAPI

# FastAPI 인스턴스 생성 
app = FastAPI()

# api 추가 (함수 등록)
# @app.get("/health")
# def health_check():
#     return {
#         "status": "ok"
#     }

# cd /Users/han/Desktop/python-digital-twin-foundations/daily/unit15_fastapi_basics         
# uvicorn unit15:app --reload
# http://127.0.0.1:8000/docs

# ------------------------------------------------------------------
# 2. GET - 조회 API
# ------------------------------------------------------------------
# HTTP 요청의 정보: Method, Path, Headers, Body
# HTTP Method: GET, POST, PUT, PATCH, DELETE

# GET
# /devices/PUMP-01
# {device_id}가 패스 파라미터: 받아서 매개변수로 전달 
# @app.get("/devices/{device_id}")
# def get_device(device_id: str):
#     return DEVICES[device_id]

# 실습
# [GET] /devices/{device_id}/status

@app.get("/devices/{device_id}/status")
def get_device_status(device_id: str):
    return {
        "device_id": device_id,
        # "status": DEVICES.get(device_id, {}).get("status", "Unknown"),
        "status": DEVICES[device_id]["status"]
    } 

# http://127.0.0.1:8000/devices/PUMP-01/status

# ------------------------------------------------------------------
# 3. HTTPException - 존재하지 않는 장비 처리 
# ------------------------------------------------------------------
# 서버 고장(500 Internal Server Error)으로 퉁치는 대신에, 
# 명확한 웹 표준 에러(404 Not Found)로 상황을 전달할 수 있음 

from fastapi import HTTPException

@app.get("/devices/{device_id}")
def get_device(device_id: str):
    if device_id not in DEVICES:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )
    return DEVICES[device_id]


# | `200` | 정상 처리        
# | `201` | 생성 성공        
# | `400` | 잘못된 요청       
# | `404` | 대상 없음        
# | `422` | 요청 데이터 검증 실패 
# | `500` | 서버 내부 오류     

# ------------------------------------------------------------------
# 4. POST - 센서 측정값 전달과 Pydantic 모델
# ------------------------------------------------------------------
# POST /devices/PUMP-01/measurements

# 전달할 데이터 (HTTP 요청의 Body로 들어감)
{
  "sensor_type": "temperature",
  "value": 35.2
}

from pydantic import BaseModel

# 검증을 위한 요청 구조 정의 (BaseModel 상속받은 클래스)
# Body로 받을 데이터 형태 선언
class MeasurementCreate(BaseModel):
    sensor_type: str
    value: float

@app.post(
        "/devices/{device_id}/measurements",
        status_code=201, # 생성 성공
)
def create_measurement(
    device_id: str,
    measurement: MeasurementCreate,
):
    if device_id not in DEVICES:
        raise HTTPException(
            status_code=404, 
            detail="Device not found",
        )

    device = DEVICES[device_id]
    status = classify_temperature(measurement.value)

    new_measurement = {
        "sensor_type": measurement.sensor_type,
        "value": measurement.value,
        "status": status,
    }

    device["measurements"].append(new_measurement)
    device["status"] = status

    return new_measurement

# request URL
# http://127.0.0.1:8000/devices/PUMP-01/measurements

# Request body 
{
  "sensor_type": "temperature",
  "value": 60.4
}

# Response body
{
  "sensor_type": "temperature",
  "value": 60.4,
  "status": "critical"
}

# "60.4"를 입력하면, 자동으로 60.4로 처리되어 생성 성공됨
# "abc"를 입력하면, 422 Unprocessable Content 요청 데이터 검증 실패 에러 발생함 
