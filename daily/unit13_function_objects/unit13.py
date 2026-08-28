# ==================================================================
# Unit 13 - 함수 객체와 고차 함수
# ==================================================================
def classify_temperature(value: float) -> str:
    if value >= 40:
        return "critical"
    if value >= 30:
        return "warning"
    return "normal"


def classify_vibration(value: float) -> str:
    if value >= 8:
        return "critical"
    if value >= 5:
        return "warning"
    return "normal"

# ------------------------------------------------------------------
# 1. '함수도 객체다'가 중요한 이유
# ------------------------------------------------------------------
# 함수 실행
result = classify_temperature(35)

# 변수에 함수 넣을 수 있다 (실행x)
classifier = classify_temperature

print(classifier(35)) # warning

# 왜 유용할까 

# 기존의 코드에서는 센서타입이 늘어나면 코드도 추가해야함
def classify_status(sensor_type: str, value: float) -> str:
    if sensor_type == "temperature":
        return classify_temperature(value)

    if sensor_type == "vibration":
        return classify_vibration(value)

    if sensor_type == "pressure":
        ...

    raise ValueError("지원하지 않는 센서 타입입니다.")

# 함수 객체를 이용해서 센서 타입과 동작을 연결
# 조건문이 동작을 선택하는 대신, 데이터 구조가 동작을 선택

# 매핑 테이블(라우터)
CLASSIFIERS = {
    "temperature": classify_temperature,
    "vibration": classify_vibration,
}

def classify_status(sensor_type:str, value: float) -> str:
    classifier = CLASSIFIERS[sensor_type]
    return classifier(value)

status = classify_status("temperature", 34.5)
print(status)

# 조건문 대비 딕셔너리 매핑/전략 패턴의 장점: 확장성, 가독성, 성능
# 그럼 언제 써야하나?
# 1. 1:1 매칭일 때, 앞으로 종류가 늘어날 가능성이 높을 때, 
# 반대로 논리가 복잡하거나, 조건이 3개 이상으로 더 늘어날 일이 없을 때 

# 실습
def classify_humidity(value: float) -> str:
    if value >= 80:
        return "critical"
    elif value >= 60:
        return "warning"
    return "normal"

CLASSIFIERS = {
    "temperature": classify_temperature,
    "vibration": classify_vibration,
    "humidity": classify_humidity,
}

assert classify_status("humidity", 50) == "normal"
assert classify_status("humidity", 65) == "warning"
assert classify_status("humidity", 85) == "critical"


# ------------------------------------------------------------------
# 2. 고차 함수
# ------------------------------------------------------------------
# 고차 함수란?
# 1. 함수를 인자로 받는다
# 2. 함수를 반환한다
