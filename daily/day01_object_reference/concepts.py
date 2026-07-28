# ===============================================
# 1. 상태 조회 
# ===============================================
device = {
    "id": "PUMP-01",
    "status": "normal", 
    "measurements": [24.5, 26.5],
    "metadata": {
        "location": "ROOM-A"
    },
}
original_id = id(device)

print(device["id"])
print(device["status"])
print(device["measurements"])

# ===============================================
# 2. 상태변경
# ===============================================
device["status"] = "warning" # 딕셔너리 내부 값을 수정할 뿐임 
new_id = id(device)
print(original_id == new_id) # True 

# 재할당이 되는 경우 
device = { 
    "id": "PUMP-02",
    "status": "normal",
    "measurements": [],
    "metadata": {
        "location": "ROOM-B",
    },
}
new_id = id(device)
print(original_id == new_id) # False 

# ===============================================
# 3. 별칭문제 
# ===============================================
backup = device # 둘은 같은 딕셔너리를 가르키는 상태
backup["status"] = "critical" # 딕셔너리 내부 값을 수정함 

print(device["status"])
print(backup["status"])
print(device is backup) # True - 여전히 하나의 딕셔너리 객체를 가르키고 있음으로

# ===============================================
# 4. '==' 와 'is'  
# ===============================================
device_a = {
    "id": "PUMP-01",
    "status": "normal",
}

device_b = {
    "id": "PUMP-01",
    "status": "normal",
}

# 가변변수(Mutable): 딕셔너리, 리스트, 세트 
# 값이 똑같더라도 선언할 때마다 서로 다른 주소에 새 객체를 생성함 
print(device_a == device_b) # True - 값이 같다 
print(device_a is device_b) # False - 같은 객체는 아니다 


# 불가변변수(Immutable): 정수, 문자열, 튜플
# 동일한 값이라면 메모리를 아끼기 위해 주소를 공유(재사용)함
a = 'str'
b = 'str'
print(a == b) # True - 값이 같다 
print(a is b) # True - 같은 주소 공유 중 

# ===============================================
# 5. 얕은 복사의 문제 copy()
# ===============================================
device = {
    "id": "PUMP-01",
    "status": "normal",
    "measurements": [24.5, 25.1],
    "metadata": {
        "location": "ROOM-A",
    },
}

backup = device.copy()

print(device == backup) # True
print(device is backup) # False 

# 주소값이 개별적임으로 값을 독립적으로 수정할 수 있다 
backup["status"] = "critical"

print(device["status"]) # normal
print(backup["status"]) # critical - 독립적으로 수정됨 

# 중첩 리스트를 수정한다면?
backup["measurements"].append(30)

print(device["measurements"]) #[24.5, 25.1, 30]
print(backup["measurements"]) #[24.5, 25.1, 30] - 여전히 같은 객체라 동시 수정된 것

# 즉 copy()는 바깥쪽 딕셔너리만 복사함 
# 내부의 딕셔너리나 리스트는 여전히 같은 주소가 할당되어진 상태 

# ===============================================
# 6. 깊은 복사 
# ===============================================
from copy import deepcopy # 또는 그냥 객체를 새로 만든다 

device = {
    "id": "PUMP-01",
    "status": "normal",
    "measurements": [24.5, 25.1],
    "metadata": {
        "location": "ROOM-A",
    },
}

backup = deepcopy(device)

backup["measurements"].append(30)
backup["metadata"]["location"] = "ROOM-B"

print(device)
print(backup)

# ===============================================
# 7. 함수에서 원본이 바뀌는 이유
# ===============================================
def add_measurement(device, value):
    # 딕셔너리 내부 값 수정 
    device["measurements"].append(value)

device = {
    "id": "PUMP-01",
    "status": "normal",
    "measurements": [],
    "metadata": {},
}

add_measurement(device, 28.4)
print(device["measurements"]) # 28.4 - 수정된 값으로 출력됨 

def replace_device(device):
    # 지역번수 'device'는 새 딕셔너리 생성하여 그 주소를 바라봄 
    device = {
    "id": "PUMP-99",
    "status": "critical",
    "measurements": [],
    "metadata": {},
}

device = {
    "id": "PUMP-01",
    "status": "normal",
    "measurements": [],
    "metadata": {},
}

replace_device(device)
print(device["id"]) # PUMP-01

# ===============================================
# 8. 부작용 없는 함수로 수정
# ===============================================
def add_measurement(device, value):
    updated_device = deepcopy(device) # 깊은 복사 
    updated_device["measurements"].append(value) 
    return updated_device

original = {
    "id": "PUMP-01",
    "status": "normal",
    "measurements": [],
    "metadata": {},
}

updated = add_measurement(original, 27.5)

print(original["measurements"]) # []
print(updated["measurements"]) #[27.5]

# ===============================================
# 9. 가변 기본 인자 문제 
# ===============================================
def create_device(
        device_id,
        measurements = [] # 이게 재사용되어짐(같은 주소 할당)
):
    return {
        "id":
         device_id,
         "status": "normal",
         "measurements": measurements 
    }

device_a = create_device("PUMP-01")
device_b = create_device("PUMP-02")

device_a["status"] = "critical"
device_a["measurements"].append(25.0)

print(device_b["status"]) # normal - 값 안바뀜 
print(device_b["measurements"]) # [25.0] - 같이 바뀜 

print(device_a is device_b) # False - 딕셔너리 자체는 독립적임 
print(device_a["measurements"] is device_b["measurements"]) # True - 내부 리스트는 같은 주소 상태 

# 수정된 함수 
def create_device(
        device_id,
        measurements=None
):
    if measurements is None:
        measurements = []

    return {
            "id":
             device_id,
             "status": "normal",
             "measurements": measurements 
        }