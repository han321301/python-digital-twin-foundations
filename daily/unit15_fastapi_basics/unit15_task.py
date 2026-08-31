# ==================================================================
# 최종 실습
# ==================================================================
# GET /devices/{device_id}/latest-measurements
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# 데이터
DEVICES = {
    "PUMP-01": {
        "device_id": "PUMP-01",
        "name": "Cooling Pump",
        "status": "warning",
        "measurements": [
            {
                "sensor_type": "temperature",
                "value": 28.5,
                "status": "normal",
            },
            {
                "sensor_type": "vibration",
                "value": 4.1,
                "status": "normal",
            },
            {
                "sensor_type": "temperature",
                "value": 35.2,
                "status": "warning",
            },
            {
                "sensor_type": "vibration",
                "value": 6.3,
                "status": "warning",
            },
            {
                "sensor_type": "pressure",
            },
        ],
    }
}
print(**DEVICES["PUMP-01"])
# ------------------------------------------------------------------
# Pydantic 모델 정의
# ------------------------------------------------------------------
class Measurement(BaseModel):
    sensor_type: str
    value: float
    status: str

class Device(BaseModel):
    device_id: str
    name: str
    status: str
    measurements: list[Measurement] = Field(default_factory=list)


# ------------------------------------------------------------------
# 라우터 엔드포인트 구현
# ------------------------------------------------------------------
@app.get("/devices/{device_id}/latest-measurements")
def get_latest_measurements(device_id:str):
    if device_id not in DEVICES:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    raw_device = DEVICES[device_id]

    try:
        device = Device(**raw_device)
        # **raw_device : 키와 값을 인자 형태로 품
        # Device(device_id="PUMP-01", name="Cooling Pump", status="warning")
        # Device() : 필수 키, 타입, 유효성 겁사 통과 못하면 ValidationError 발생 
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Field required: {str(e.errors())}"
        )

    latest = {}
    for m in device.measurements:
        latest[m.sensor_type] = {
            "value": m.value,
            "status": m.status,
        }

    return {
        "device_id": device.device_id, 
        "latest_measurements": latest
    }

