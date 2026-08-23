# ==================================================================
# unit10 - 캡슐화와 @property
# ==================================================================

# ------------------------------------------------------------------
# 1. @dataclass인데 왜 캡슐화가 필요한가?
# ------------------------------------------------------------------
from dataclasses import dataclass, field

@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str
    measurements: list[float] = field(default_factory=list)

sensor = Sensor(
    sensor_id="TEMP-01",
    sensor_type="temperature",
    unit="celsius",
)

# 지금 상태에서 외부에서 가능한 동작 
sensor.measurements.append(999) #[999]
sensor.measurements.clear() #[]
sensor.measurements = None #None
print(sensor.measurements)

# add_measurement() 와 같은 메서드에서 검증 단계를 구현하더라도
# measurements에 직접 접근 가능하게 두면, 그 의미가 없어짐 

# ------------------------------------------------------------------
# 2. 내부 상태로 바꾸기
# ------------------------------------------------------------------
@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str

    # 클래스 내부용 리스트 정의 
    _measurements: list[float] = field(
        default_factory=list, # 새로운 객체가 만들어질 때마다 독립적인 빈 리스트 생성
        repr=False, # 출력 제한 옵션, 여전히 접근은 가능한 상태임 
    )

# ------------------------------------------------------------------
# 3. 상태 변경 경로 생성 
# ------------------------------------------------------------------
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
        # 검증로직 ... 
        self._measurements.append(value)

# ------------------------------------------------------------------
# 4. @property - 메서드를 속성처럼 읽기 
# ------------------------------------------------------------------
# latest_value()는 동작이라기보다 센서의 상태를 조회하는 것에 가까움 
# 그래서 `sensor.latest_value` 로 표현하는게 자연스럽다

@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str

    _measurements: list[float] = field(
        default_factory=list,
        repr=False,
    )

    def add_measurement(self, value: float) -> None:
        self._measurements.append(value)

    @property # 아래의 메서드는 속성처럼 접근 가능해짐 
    def latest_value(self) -> float | None:
        if not self._measurements:
            return None

        return self._measurements[-1]

# 사용 
sensor = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

sensor.add_measurement(28.5)
sensor.add_measurement(31.2)

print(sensor.latest_value)

# ------------------------------------------------------------------
# 5. measurements를 읽게 해주되 수정은 못 하게 만들기
# ------------------------------------------------------------------
@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str

    _measurements: list[float] = field(
        default_factory=list,
        repr=False,
    )

    def add_measurement(self, value: float) -> None:
        self._measurements.append(value)

    # 외부접근용으로 만들어줌
    @property 
    def measurements(self):
        return self._measurements 


sensor = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

sensor.add_measurement(28.5)
sensor.add_measurement(31.2)

sensor.measurements.clear()
print(sensor.measurements)  # [] 외부에서 _measurements를 비워버림

# 해결 방법 1 - 복사본 반환 => 여전히 수정 행위(append, clear 등)은 가능함 
# `return self._measurments.copy()`

# 해결 방법 2 - tuple로 반환 => 불변 객체임으로 외부에서 수정할 수 없음 
# `return tuple(self._measurements)`

# ------------------------------------------------------------------
# 6. 공개 인터페이스 결정하기
# ------------------------------------------------------------------
# 당장 검증이나 계산 필요 없는 것
# : sensor_id, sensor_type, unit 

# 검증 로직이 필요한 것(@property 적용할 것)
# : measurements, latest_value, measurement_count

# ------------------------------------------------------------------
# 7. setter 로 유효성 검사 
# ------------------------------------------------------------------
@dataclass
class Sensor:
    sensor_id: str # @property로 함수 버튼으로 작동됨 

    @property
    def sensor_id(self): # 함수로 정의되는 sensor_id
        return self._sensor_id

    @sensor_id.setter
    def sensor_id(self, value: str):
        if not isinstance(value, str):
            raise TypeError("id는 문자여야 합니다.")
        self._sensor_id = value # id를 담는 진짜 데이터 상자 선언 

sensor = Sensor("abc1234")
sensor.sensor_id = "abc"

print(f"sensor_id: {sensor.sensor_id}")

# setter가 아래에 있어도, 실제 실행될 때는 세터가 먼저 실행됨
# setter는 변수 선언없이 동적으로 즉시 변수를 새로 생성한다.
# `self._sensor_id = value`를 실행하는 순간 동적으로 변수를 만듬 
