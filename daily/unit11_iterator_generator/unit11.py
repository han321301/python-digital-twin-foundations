# 복습
from dataclasses import dataclass, field

@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str

    _measurements: list[float] = field(
        default_factory=list,
        repr=False
    )

    def add_measurement(self, value: float) -> None:
        self._measurements.append(value)

    @property
    def measurements(self):
        return self._measurements

    @property 
    def unit(self):
        return self.unit

    @unit.setter
    def unit(self, value: str):
        if not isinstance(value, str):
            raise TypeError("")
        self._unit = value 

# ==================================================================
# unit11 - iterator and generator
# ==================================================================
records = [
    {
        "sensor_id": "TEMP-01",
        "value": "28.5",
    },
    {
        "sensor_id": "TEMP-01",
        "value": "31.2",
    },
    {
        "sensor_id": "TEMP-01",
        "value": "45.8",
    },
    {
        "sensor_id": "TEMP-01",
        "value": "29.7",
    },
]

# ------------------------------------------------------------------
# 1. 지금 방식의 문제 확인 - 데이터가 100,000건이라면? 
# ------------------------------------------------------------------
# 현재 방식: 측정값을 append()로 리스트에 저장한다 
# 문제 :
# - 10만건이 전부 처리될 때까지 처섭ㄴ째 결과조차 받을 수 없는 구조 
# - 그리고 전체 결과가 필요하지 않는 상황(이상치 찾기)에도 전체 데이터가 처리를 거치게 됨 

# ------------------------------------------------------------------
# 2. generator 전에 iterator 알기 (for문)
# ------------------------------------------------------------------
values = [10,20,30]

for value in values: 
    ...

# for문 내부 작동 원리:
# 1. iter() ->  next() -> StopIteration 

iterator = iter(values)  # 1. 반복자(Iterator) 생성

print(next(iterator)) #10
print(next(iterator)) #20
print(next(iterator)) #30 - iterator가 현재 어디까지 읽었는지 기억하며 작동
# print(next(iterator)) # StopIteration 에러 발생

# for문 실행했을 때 파이썬이 자동으로 작동하는 코드 
while True:
    try:
        value = next(iterator)  # 2. 다음 아이템 추출
        print(value)
    except StopIteration:  # 3. 끝에 도달하면 종료
        break

# Iterable: for문이 순회할 수 있는 객체(list, tuple, dict, str, set) 
# Iterator: next()를 사용해서 한단게를 전진하여 다음 순서의 데이터를 꺼내 주는 생성기, 재사용불가(순회불가)

# Iterator를 구현해주는 기능 => yield 

# ------------------------------------------------------------------
# 3. yield로 센서 데이터 한 건씩 제공하기 
# ------------------------------------------------------------------
def read_measurements(records):
    for record in records:
        measurement = {
            "sensor_id": record["sensor_id"],
            "value": float(record["value"]),
        }
        yield measurement # yield의 기능 : 값 반환 후 일시정지 

# 1. Generator 생성, 함수를 실행 시키지 않음
stream = read_measurements(records) 

print(f"stream: {stream}") 
# <generator object read_measurements at 0x102bc0d40>

# 함수 내부 코드 실행 시작 
# 이처럼 요구될 때까지 계산을 미루는 방식을 지연평가라 한다 
# 미리 메모리를 쓰지 않고 효율적으로 대기할 수 있다
print(next(stream)) 

# 일시정지된 코드를 다시 실행 
# yield가 있던 그 자리(반복문)으로 돌아간다 
print(next(stream))

# 실습 
def read_measurements(records):
    for record in records:
        measurement = {
            "sensor_id": record["sensor_id"],
            "value": float(record["value"]),
        }

        yield measurement

stream = read_measurements(records)

print(next(stream))
print(next(stream))

# ------------------------------------------------------------------
# 5.제너레이터 주의점
# ------------------------------------------------------------------
# 제너레이터는 실행 위치를 기억하고, 누를 때마다 하나씩 꺼내주는 재생버튼 같은 것

# Generator: 대량 데이터를 한번만 순차 처리할 때, 스트리밍 데이터 
# List: 결과를 여러번 사용할 예정, 인덱스로 접근해야 할 때 

# 저장할 필요가 있다면 리스트로 변환할 수 있음
measurements = list(read_measurements(records))

print(f"measurements: {measurements}")
