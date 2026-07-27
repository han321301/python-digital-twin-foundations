from copy import deepcopy

# ===============================================
# 최종 구현 과제
# ===============================================

# 1. 장비 생성 
def create_device(device_id, location):
    return {
        "id": device_id,
        "status": "normal",
        "measurements": [],
        "metadata": {"location": location}
    }

device = create_device("PUMP-01", "ROOM-A")

# 2. 측정값 추가 및 상태 자동 계산
def add_measurement(device, value):
    updated_device = deepcopy(device)

    status = "normal" if value < 30 else ("warning" if value < 40 else "critical")

    updated_device["status"] = status 
    updated_device["measurements"].append(value)
    return updated_device

updated = add_measurement(device, 30)
print(updated)
print(device)

# 3. 원본 보존 확인
original = create_device("PUMP-01", "ROOM-A")
updated = add_measurement(original, 35.0)

assert original["measurements"] == []
assert original["status"] == "normal"

assert updated["measurements"] == [35.0]
assert updated["status"] == "warning"

assert original is not updated
assert (
    original["measurements"] is not updated["measurements"]
)