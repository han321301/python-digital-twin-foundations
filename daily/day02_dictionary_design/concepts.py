# # ==================================================================
# # day02 dictionary_design
# # ==================================================================

# ------------------------------------------------------------------
# 1. 장비 여러 대를 어떻게 저장할까 
# ------------------------------------------------------------------

# 리스트 
device_list = [
    {
        "id": "PUMP-01",
        "name": "냉각수 펌프",
        "location": "ROOM-A",
    },
    {
        "id": "FAN-01",
        "name": "배기 팬",
        "location": "ROOM-B",
    },
    {
        "id": "MOTOR-01",
        "name": "컨베이어 모터",
        "location": "ROOM-C",
    },
]

# 딕셔너리
device_registry = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "location": "ROOM-A",
    },
    "FAN-01": {
        "name": "배기 팬",
        "location": "ROOM-B",
    },
     "MOTOR-01": {
        "name": "컨베이어 모터",
        "location": "ROOM-C",
    },
}

assert len(device_registry) == 3
assert device_registry["FAN-01"]["location"] == "ROOM-B"
assert "MOTOR-01" in device_registry


# ------------------------------------------------------------------ 
# 2. 딕셔너리 조회 방법
# ------------------------------------------------------------------
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "location": "ROOM-A",
        "status": "normal",
    },
    "FAN-01": {
        "name": "배기 팬",
        "location": "ROOM-B",
        "status": "warning",
    },
}

pump = factory["PUMP-01"]
# pump = factory["MOTER-99"]
# print(pump) # KeyError - 없는 키를 조회하면 에러남
# 반드시 존재해야하는 데이터에 적합 

# 값을 찾는 다른 방식 'get()'
# 데이터가 없어도 정상적인 상황에 적합
device = factory.get("PUMP-01") 

device = factory.get("MOTER-99") 
print(device) # None - 없는 키라도 에러가 나지 않음 

# 키 존재를 검사하는 'in' 
if "PUMP-01" in factory:
    print(factory["PUMP-01"])

# 안전한 조회 함수
def find_device(
        factory: dict,
        device_id: str,
) -> dict | None:
    if device_id in factory:
        return factory[device_id]

# 검증
assert find_device(factory, "PUMP-01") == {
    "name": "냉각수 펌프",
    "location": "ROOM-A",
    "status": "normal",
}

assert find_device(factory, "UNKNOWN") is None

unknown = {
    "name": "알 수 없음", "sensors": [],
}

device_a = factory.get("A", unknown)
device_b = factory.get("B", unknown)

device_a["sensors"].append("TEMP-99")

print(device_a) # {'name': '알 수 없음', 'sensors': ['TEMP-99']}
# 키가 존재 하지 않는 경우 두 번째 인자로 넘겨준 객체의 주소(참조)를 그대로 반환함 

print(device_a is device_b) # True


# ------------------------------------------------------------------
# 3. 장비 등록과 수정
# ------------------------------------------------------------------
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "location": "ROOM-A",
        "status": "normal",
    },
    "FAN-01": {
        "name": "배기 팬",
        "location": "ROOM-B",
        "status": "warning",
    },
}

# 값 일부만 수정하기
factory["PUMP-01"]["status"] = "critical"
print(factory["PUMP-01"]) 
# {'name': '냉각수 펌프', 'location': 'ROOM-A', 'status': 'critical'}

# update()로 일부만 수정하기
# 기존 딕셔너리를 변경하고 None을 반환하는 함수 
factory["PUMP-01"].update({
    "status": "normal",
    "location": "ROOM-D",
})
print(factory["PUMP-01"]) 
# {'name': '냉각수 펌프', 'location': 'ROOM-D', 'status': 'normal'}

# 장비 등록하기
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
        "status": "normal",
        "sensors": {},
    }

    return True

# 검증
factory = {}

assert register_device(
    factory,
    "PUMP-01",
    "냉각수 펌프",
    "ROOM-A",
) is True

assert register_device(
    factory,
    "PUMP-01",
    "새 펌프",
    "ROOM-B",
) is False

assert factory["PUMP-01"]["name"] == "냉각수 펌프"


# ------------------------------------------------------------------
# 4. 중첩 딕셔너리와 센서 등록
# ------------------------------------------------------------------
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "location": "ROOM-A",
        "status": "normal",
        "sensors": {},
    },
}

# 센서 등록
factory["PUMP-01"]["sensors"]["TEMP-01"] = {
    "type": "temperature",
    "unit": "celsius",
}

# 센서 등록 함수
def register_sensor(
        factory: dict,
        device_id: str,
        sensor_id: str,
        sensor_type: str,
        unit: str,
) -> bool:
    if device_id not in factory:
        return False

    if sensor_id in factory[device_id]:
        return False

    factory[device_id][sensor_id] = {
        "sensor_type": sensor_type,
        "unit": unit,
    }

    return True

# 검증 
factory = {}

register_device(
    factory,
    "PUMP-01",
    "냉각수 펌프",
    "ROOM-A",
)

assert register_sensor(
    factory,
    "PUMP-01",
    "TEMP-01",
    "temperature",
    "celsius",
) is True

assert register_sensor(
    factory,
    "PUMP-01",
    "TEMP-01",
    "temperature",
    "celsius",
) is False

assert register_sensor(
    factory,
    "UNKNOWN",
    "TEMP-02",
    "temperature",
    "celsius",
) is False


# ------------------------------------------------------------------
# 5. setdefault()는 언제 쓰는가?
# ------------------------------------------------------------------
legacy_device = {
    "name": "구형 펌프",
    "location": "ROOM-X",
}

# KeyError: 'sensors'발생
# legacy_device["sensors"]["TEMP-01"] = {
#     "type": "temperature",
# } 

# 해결 방법 
if "sensor" not in legacy_device:
    legacy_device["sensors"] = {}

legacy_device["sensors"]["TEMP-01"] = {
    "type": "temperature",
}

# setdefault() 방식으로 해결하기
# 기존 딕셔너리에 키가 없으면 기본값을 새로 만들어 넣음 
# 키가 이미 있다면 저장된 값을 그대로 꺼내옴 
sensors = legacy_device.setdefault("sensors", {})
sensors["TEMP-01"] = {"type": "temperature"}
print(legacy_device["sensors"]) 
# {'TEMP-01': {'type': 'temperature'}}

# default().append() - 순서 있는 목록일 때 
# .append() 쓰면 안되고 []할당을 해야하는 경우 => 값이 딕셔너리 일 때

# 'PUMP-01'이 없다면 만들고 빈배열을 값으로 함 -> 값 추가 
# 이미 있다면 값만 추가 
device_history = {}
device_history.setdefault("PUMP-01", []).append("2026-07-28: STARTED")
device_history.setdefault("PUMP-01", []).append("2026-07-28: STOPPED")

print(device_history) 
# {'PUMP-01': ['2026-07-28: STARTED', '2026-07-28: STOPPED']}

# 실습 
# - sensors 키가 없으면 빈 딕셔너리 생성
# - 있다면 기존 딕셔너리를 유지 
# - 센서 딕셔너리 반환 
def ensure_sensor_registry(device: dict) -> dict:
    if "sensors" in device:
        return device["sensors"]

    return device.setdefault("sensors", {})

# 검증 
device = {
    "name": "냉각수 펌프",
}

sensors = ensure_sensor_registry(device)

assert sensors == {}
assert device["sensors"] is sensors

sensors["TEMP-01"] = {
    "type": "temperature",
}

assert "TEMP-01" in device["sensors"]

# ------------------------------------------------------------------
# 6. 왜 딕셔너리 키에는 리스트를 쓸 수 없을까?
# ------------------------------------------------------------------
# 리스트: 가변 객체 => 키로 사용 불가능
# 튜플: 불변 객체 = 해시값 고정 => 딕셔너리 키로 사용 가능

print("hashed: ", hash(("room-a", "device-01"))) # hashed: 4190208832014483238
# print("hashed: ", hash["room-a", "device-01"]) # TypeError

# *해시값은 데이터가 메모리 상의 어느 위치(주소)에 들어가야 하는지 즉시 계산해주는 '수학적 이정표(키)' 역할
# 불변 객체를 넣으면 고유한 정수값을 반환하고, 가변 객체를 넣으면 에러남 

# [추가] 튜플을 키로 사용하는 예시
# 예시 1. (X좌표, Y좌표)를 키로 사용
grid = {}
grid[(0, 0)] = "Start"
# 예시 2. 복합식별자 (공장ID, 장치ID) 조합으로 상태 관리
device_status = {
    ("FACTORY-A", "PUMP-01"): "running",
    ("FACTORY-A", "PUMP-02"): "stopped",
}
status = device_status[("FACTORY-A", "PUMP-01")]


# ------------------------------------------------------------------
# 7. 장비 목록은 리스트인가, 딕셔너리인가?
# ------------------------------------------------------------------
# 키값이 되는 고유 아이디로 빠른 검색이 필요하다 => 딕셔너리
# 순서가 있는 단순 목록 => 리스트 


# ------------------------------------------------------------------
# 8. 삭제 방식
# ------------------------------------------------------------------
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
        "location": "ROOM-A",
        "status": "normal",
    },
    "FAN-01": {
        "name": "배기 팬",
        "location": "ROOM-B",
        "status": "warning",
    },
}

# del
# del factory["PUMP-01"]

# pop()
removed = factory.pop("FAN-01")

# removed = factory.pop("FAN-01") # KeyError
removed = factory.pop("FAN-01", {}) # 키가 없을 때의 기본값을 빈 딕셔너리로 지정
print(removed) # {}

# 삭제 함수
def remove_device(
        factory: dict,
        device_id: str,
) -> dict | None:
    return factory.pop(device_id, None)

# 검증
factory = {
    "PUMP-01": {
        "name": "냉각수 펌프",
    },
}

removed = remove_device(
    factory,
    "PUMP-01",
)

assert removed == {
    "name": "냉각수 펌프",
}

assert "PUMP-01" not in factory
assert remove_device(factory, "UNKNOWN") is None

print("factory : ", factory) # {}
