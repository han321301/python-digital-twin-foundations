# ==================================================================
# Unit 09 - dataclass and composition
# ==================================================================
# - 단일 Sensor 클래스를 확장해서, Device가 여러 Sensor 객체를 관리하는 구조
# - 장비에 센서를 등록하고, 센서 상태를 이용해 장비 전체 상태를 계산하는 기능



# ------------------------------------------------------------------
# 1. 표준 라이브러리 dataclasses는 언제 쓰는가
# ------------------------------------------------------------------
# 직접 클래스 정의하는 경우
# 기본적인 메서드를 직접 작성해야함, 출력도 읽기 좋지 않음
class Sensor:
    def __init__(
        self,
        sensor_id,
        sensor_type,
        unit,
    ):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit

sensor = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

print(sensor) 
# <__main__.Sensor object at 0x1015d86e0>


# 표준 라이브러리 dataclasses
# __init__, __repr__, __eq__ 와 같은 메서드를 자동 생성해줌 
from dataclasses import dataclass, field

@dataclass
class Sensor: 
    # 아래 선언을 바탕으로 __init__이 생성됨 
    sensor_id: str
    sensor_type: str
    unit: str 
    status: str = "normal" # 기본값 주기 

sensor = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

print(sensor) 
# Sensor(sensor_id='TEMP-01', sensor_type='temperature', unit='celsius')

# dataclasses 쓰지 않는게 좋은 상황
# - 저장보다는 메서드 중심의 클래스일 때 

# ------------------------------------------------------------------
# 2. 기본값을 딕셔너리/리스트로 설정하기
# ------------------------------------------------------------------
# PUMP-01
# ├── TEMP-01
# ├── VIB-01
# └── PRESS-01

@dataclass
class Device:
    device_id: str
    name: str
    # measurements: dict = {} 
    # 여러 인스턴스가 같은 딕셔너리르 공유할 위험이 있음
    # 가변 객체(리스트와 딕셔너리)는 파이썬에서 기본값으로 지정할 수 없음 
    # 이렇게가 아니라  dict() 활용해서 작성
    # field()는 dataclass 세밀하게 설정할 때 사용
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

device = Device(
    device_id="PUMP-01",
    name="냉각수 펌프",
)

print(device.sensors) # {}


# ------------------------------------------------------------------
# 3. 센서등록 기능 추가하기
# ------------------------------------------------------------------
@dataclass
class Device:
    device_id:str
    name: str
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

    def add_sensor(
            self, sensor: Sensor,
    ) -> None:
        self.sensors[sensor.sensor_id] = sensor

device = Device(
    "PUMP-01",
    "냉각수 펌프",
)

sensor = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
)

device.add_sensor(sensor)

print(device.sensors)

# ------------------------------------------------------------------
# 4. 중복 센서 처리 
# ------------------------------------------------------------------
# 에러 정의
class SensorAlreadyExistsError(Exception):
    pass

# 에러 처리 추가 
@dataclass
class Device:
    device_id: str
    name: str
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

    def add_sensor(
        self,
        sensor: Sensor,
    ) -> None:

        # 센서아이디가 이미 센서 딕셔너리에 존재한다면, raise
        if sensor.sensor_id in self.sensors:
            raise SensorAlreadyExistsError(
                f"[ERROR] 이미 등록된 센서입니다: {sensor.sensor_id}"
            )
        
        # 아닌 경우 등록 실행 
        self.sensors[sensor.sensor_id] = sensor

# device = Device(
#     "PUMP-01",
#     "냉각수 펌프",
# )

# device.add_sensor(
#     Sensor(
#         "TEMP-01",
#         "temperature",
#         "celsius",
#     )
# )

# device.add_sensor(
#     Sensor(
#         "TEMP-01",
#         "temperature",
#         "fahrenheit",
#     )

# ------------------------------------------------------------------
# 5. 센서 조회 기능 추가하기
# ------------------------------------------------------------------
class SensorNotFoundError(Exception):
    """존재하지 않는 센서"""


@dataclass
class Device:
    device_id: str
    name: str
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

    def get_sensor(self, sensor_id: str) -> Sensor:
        sensor = self.sensors.get(sensor_id)

        if sensor is None: 
            raise SensorNotFoundError(
                f"센서를 찾을 수 없습니다: {sensor_id}"
            )

        return sensor

# device = Device(
#     "PUMP-01",
#     "냉각수 펌프",
# )

# device.get_sensor("TEMP-01")

# ------------------------------------------------------------------
# 6. 합성과 상속 
# ------------------------------------------------------------------
# 상속 관계: Is-A, 강한 결합, 부모의 기능을 그대로 물려받음 class Child(Parent):
# 전자기기 > 스마트폰 

# 합성 관계: Has-A, 느슨한 결합, 다른 객체를 가져와 조립하는 개념 self.compoment = component()
# 스마트폰은 배터리를 가지고 있음 

# 무엇을 써야할까? 
# 상속보다는 합성을 우선하라 
# 상속은 관계가 평생 변하지 않고 계층구조일때만 

# ------------------------------------------------------------------
# 7. 장비 전체 상태 계산
# ------------------------------------------------------------------
# 센서 여러개 중 상태가 심각한 것을 장치의 상태로 친다 
# 여기서는 온도의 warning이 장치의 상태값이 됨 
temp = Sensor(
    "TEMP-01",
    "temperature",
    "celsius",
    status="warning",
)

vibration = Sensor(
    "VIB-01",
    "vibration",
    "mm/s",
    status="normal",
)

# 우선순위 정의 
STATUS_PRIORITY = {
    "normal": 0,
    "warning": 1,
    "critical": 2,
}

# 메서드 작성 
@dataclass
class Device:
    device_id: str
    name: str
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

    def add_sensor(
            self,
            sensor: Sensor,
        ) -> None:

        self.sensors[sensor.sensor_id] = sensor 


    def overall_status(self) -> str:
        if not self.sensors:
            return "unknown"

        return max(
            self.sensors.values(), # 딕셔너리의 값들만 
            key=lambda sensor: STATUS_PRIORITY[sensor.status] # 값 중에서 status만
        ).status

device = Device(
    "PUMP-01",
    "냉각수 펌프",
)

device.add_sensor(temp)
device.add_sensor(vibration)

print(device.overall_status())

# ------------------------------------------------------------------
# 8. 최종 코드 
# ------------------------------------------------------------------
from dataclasses import dataclass, field


STATUS_PRIORITY = {
    "normal": 0,
    "warning": 1,
    "critical": 2,
}


class SensorAlreadyExistsError(Exception):
    pass


class SensorNotFoundError(Exception):
    pass


@dataclass
class Sensor:
    sensor_id: str
    sensor_type: str
    unit: str
    status: str = "normal"


@dataclass
class Device:
    device_id: str
    name: str
    sensors: dict[str, Sensor] = field(
        default_factory=dict
    )

    def add_sensor(
        self,
        sensor: Sensor,
    ) -> None:

        if sensor.sensor_id in self.sensors:
            raise SensorAlreadyExistsError(
                f"이미 등록된 센서입니다: "
                f"{sensor.sensor_id}"
            )

        self.sensors[
            sensor.sensor_id
        ] = sensor

    def get_sensor(
        self,
        sensor_id: str,
    ) -> Sensor:

        sensor = self.sensors.get(sensor_id)

        if sensor is None:
            raise SensorNotFoundError(
                f"센서를 찾을 수 없습니다: "
                f"{sensor_id}"
            )

        return sensor

    def overall_status(self) -> str:
        if not self.sensors:
            return "unknown"

        most_severe_sensor = max(
            self.sensors.values(),
            key=lambda sensor: STATUS_PRIORITY[
                sensor.status
            ],
        )

        return most_severe_sensor.status

# ------------------------------------------------------------------
# 10. 구현 과제
# ------------------------------------------------------------------
# replace_sensor() 
# 센서가 고장나서 교체한 상황: TEMP-01 -> TEMP-02

# 요구사항
# 기존은 삭제하고 새로 등록함
# 기존 객체를 반환함 
# 에러 핸들링 - 기존 센서가 없다면 낫파운드, 새 센서가 이미 존재하면 얼레디

# 주의: 모든 검증 통과 후에 삭제한다 
# 기존 센서 존재 확인 -> 새 센서 중복 확인 -> 기존 센서 삭제 -> 새 센서 등록 -> 기존 센서 반환


# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------


# ------------------------------------------------------------------
# 
# ------------------------------------------------------------------
