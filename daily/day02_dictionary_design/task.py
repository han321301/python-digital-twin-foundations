# ------------------------------------------------------------------
# 9. 오늘의 통합 과제
# ------------------------------------------------------------------

# factory = {
#     "PUMP-01": {
#         "name": "냉각수 펌프",
#         "location": "ROOM-A",
#         "sensors": {
#             "TEMP-01": {
#                 "type": "temperature",
#                 "unit": "celsius",
#             },
#             "VIB-01": {
#                 "type": "vibration",
#                 "unit": "mm/s",
#             },
#         },
#     },
# }

def register_device(
    factory: dict,
    device_id: str,
    name: str,
    location: str,
) -> bool:
    if device_id in factory:
        return False
    
    factory[device_id] = {
        "name": name,
        "location": location,
    }
    return True


def find_device(
    factory: dict,
    device_id: str,
) -> dict | None:
    return factory.get(device_id)


def register_sensor(
    factory: dict,
    device_id: str,
    sensor_id: str,
    sensor_type: str,
    unit: str,
) -> bool:
    device = factory.get(device_id)

    if device is None:
        return None 

    sensors = device.setdefault("sensors", {})

    # 이미 존재함 
    if sensor_id in sensors:
        return False 
    
    # 새로 등록하기
    sensors[sensor_id] = {
        "type": sensor_type,
        "unit": unit,
    }

    return True


def remove_sensor(
    factory: dict,
    device_id: str,
    sensor_id: str,
) -> dict | None:
    device = factory[device_id]
    if device_id is None:
        return None 

    sensors = device.get("sensors")

    if sensors is None:
        return None
    
    return sensors.pop(sensor_id, None)


def list_sensor_ids(
    factory: dict,
    device_id: str,
) -> list[str]:
    device = factory[device_id]

    if device is None: 
        return []

    sensors = device.get("sensors", {})
    return list(sensors)

factory = {}
result = factory.setdefault("pump01", [1,2,3])
print("result:", result)
print("factory:" , factory)
