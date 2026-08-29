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
# 반대로 논리가 복잡하거나, 조건이 3개 이상으로 더 늘어날 일이 없을 때는 조건문

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

# 함수를 인자로 받아오는 이유
# 동일한 처리 흐름을 여러 규칙에 재사용할 때 사용
# 여기서 판정은 전달받은 함수에 맡기고 리턴할 딕셔너리의 틀만 짠다
# 세부적인 분류규칙(classifier)는 외부에서 갈아끼울 수 있게함
# 각각 다른 센서마다 결과를 포맷팅하는 함수를 따로 생성할 필요가 없게 된다.
# classify_temp(), classify_press() 이런식의 
def process_measurement(
        value: float,
        classifier, 
) -> dict:
    return {
        "value": value,
        "status": classifier(value),
    }

result = process_measurement(35, classify_temperature)
print(result) # {'value': 35, 'status': 'warning'}

# 실습 - 규칙 교체
def build_measurement(
    sensor_id: str,
    value: float,
) -> dict:
    if value >= 40:
        status = "critical"
    elif value >= 30:
        status = "warning"
    else:
        status = "normal"

    return {
        "sensor_id": sensor_id,
        "value": value,
        "status": status,
    }

# 판정은 다른 함수에 맡긴다 
def build_measurement(
        sensor_id: str,
        value: float,
        classifier,
) -> dict:
    return {
        "sensor_id": sensor_id,
        "value": value,
        "status": classifier(value)
    }

# 사용
temp = build_measurement(
    "TEMP-01",
    35,
    classify_temperature,
)

vibration = build_measurement(
    "VIB-01",
    6,
    classify_vibration,
)

print(f"temp: {temp}")
print(f"vibration: {vibration}")

# ------------------------------------------------------------------
# 3. 함수를 반환하는 함수 
# ------------------------------------------------------------------
# 센서마다의 임계치에 따라 상태 판정 함수를 생성하는 함수
def create_classfier(
        warning_threshold: float,
        critical_threshold: float,
): 
    def classifier(value: float) -> str:
        if value >= critical_threshold:
            return "critical"

        if value >= warning_threshold:
            return "warning"

        return "normal"

    return classifier

classify_temperature = create_classfier(30, 40)
classify_vibration = create_classfier(5, 8)
classify_pressure = create_classfier(100, 130)

print(classify_temperature) # <function create_classfier.<locals>.classifier at 0x10198fab0>
print(classify_temperature(50)) # critical

# ------------------------------------------------------------------
# 4. 기준값을 어떻게 기억하는가
# ------------------------------------------------------------------
# classify_temperature = create_classfier(30, 40)
# classify_temperature은 create_classfier의 리턴값인 classifier이다 
# 하지만 생성될 때의 외부값 warning_threshold, critical_threshold을 기억하기 때문에,
# 생성시에 입력했던 30, 40을 기준으로 판정할 수 있음 (클로저)

# 실습
def create_classifier(
        warning_threshold: float,
        critical_threshold: float,
):
    def classfier(value: float) -> str:
        if value >= critical_threshold:
            return "critical"

        if value >= warning_threshold:
            return "warning"
        
        return "normal"

    return classfier



# 검증
temperature_classifier = create_classifier(30, 40)
pressure_classifier = create_classifier(100, 130)

assert temperature_classifier(20) == "normal"
assert temperature_classifier(35) == "warning"
assert temperature_classifier(45) == "critical"

assert pressure_classifier(90) == "normal"
assert pressure_classifier(110) == "warning"
assert pressure_classifier(140) == "critical"