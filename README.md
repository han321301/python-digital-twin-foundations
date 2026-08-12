## 학습 방식

* 기간: 14일
* 학습 시간: 하루 2시간
* 중심 예제: 장비·센서 상태 관리 시스템
* 매일 별도의 폴더에서 학습
* 개념 학습 후 구현, 테스트, 리팩터링 진행

## 커리큘럼

### 1주 차 — 데이터와 함수 설계

| 일차 | 주제              |
| -: | --------------- |
|  1 | 객체, 참조, 가변성, 복사 |
|  2 | 딕셔너리와 자료구조 설계   |
|  3 | 함수 인자, 반환값, 부작용 |
|  4 | 조건식과 상태 규칙 모델링  |
|  5 | 반복문과 컴프리헨션      |
|  6 | 정렬, 그룹화, 최신 상태  |
|  7 | 모듈 분리와 리팩터링     |

### 2주 차 — 객체 모델링과 안정성

| 일차 | 주제             |
| -: | -------------- |
|  8 | 예외 처리와 입력 검증   |
|  9 | 클래스와 인스턴스      |
| 10 | 데이터 클래스와 객체 합성 |
| 11 | 프로퍼티와 캡슐화      |
| 12 | 반복자와 제너레이터     |
| 13 | JSON 파일 저장과 복원 |
| 14 | 테스트와 최종 리팩터링   |

## 전체 폴더 구성

python_intermediate_14days/daily
├── day01_object_reference/
├── day02_dictionary_design/
├── day03_function_design/
├── day04_rule_modeling/
├── day05_iteration_comprehension/
├── day06_sort_group_latest/
├── day07_week1_refactoring/
├── day08_exception_validation/
├── day09_class_instance/
├── day10_dataclass_composition/
├── day11_property_encapsulation/
├── day12_iterator_generator/
├── day13_json_storage/
└── day14_testing_final_refactor/

## 세부 학습 내용 
| 단원 | 폴더 제목                            | 핵심 주제                                 | 실용 예제에서 하는 일                                             | 주요 결과물                                                        |
| -: | -------------------------------- | ------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
|  1 | `unit01_object_reference`        | 객체, 참조, 가변성, 복사                       | 장비 상태를 생성·복제하고 측정값 추가 시 원본 변경 여부 비교                      | `create_device()`, `add_measurement()`, `clone_device()`      |
|  2 | `unit02_dictionary_design`       | 딕셔너리와 자료구조 설계                         | 여러 장비와 센서를 ID 기반 등록부로 관리                                 | `register_device()`, `register_sensor()`, `find_device()`     |
|  3 | `unit03_function_design`         | 함수 인자, 반환값, 부작용, 타입 힌트                | 검증·상태 판정·장비 변경을 역할별 함수로 분리                               | `validate_value()`, `classify_status()`, `update_device()`    |
|  4 | `unit04_class_instance`          | 클래스, 인스턴스, 속성, 메서드                    | 딕셔너리 센서를 `Sensor` 객체로 전환하고 상태와 동작을 묶음                    | `Sensor` 클래스                                                  |
|  5 | `unit05_iteration_comprehension` | 반복문, 컴프리헨션, `any()`, `all()`          | 여러 `Sensor` 객체에 측정값을 처리하고 이상 센서를 추출                      | `process_measurements()`, `find_abnormal_sensors()`           |
|  6 | `unit06_sort_group_latest`       | 정렬, `key`, `lambda`, 그룹화              | 측정 이력을 센서별로 묶고 최신 상태를 계산                                 | `group_measurements_by_sensor()`, `find_latest_measurement()` |
|  7 | `unit07_module_refactoring`      | 모듈 경계, import, 실행 진입점                 | 함수와 클래스를 역할별 파일로 분리하고 의존성을 정리                            | `models.py`, `services.py`, `rules.py`, `main.py`             |
|  8 | `unit08_exception_contract`      | 예외 처리, 실패 계약, 사용자 정의 예외               | 없는 장비·센서와 잘못된 측정값을 명시적으로 처리                              | `DeviceNotFoundError`, `InvalidMeasurementError`              |
|  9 | `unit09_dataclass_composition`   | `dataclass`, `default_factory`, 객체 합성 | `Measurement` 값을 객체로 만들고 `Device`가 여러 `Sensor`를 포함하도록 설계 | `Measurement`, `Device`                                       |
| 10 | `unit10_property_encapsulation`  | 프로퍼티, 캡슐화, 방어적 복사                     | 외부에서 측정 이력을 직접 훼손하지 못하도록 인터페이스 개선                        | `latest_value`, `measurements`, `calculate_overall_status()`  |
| 11 | `unit11_iterator_generator`      | iterable, iterator, generator         | 많은 측정값을 목록으로 한꺼번에 만들지 않고 순차 처리                           | `read_measurements()`, `filter_abnormal()`                    |
| 12 | `unit12_json_storage`            | 파일, JSON, `pathlib`, `with`, 직렬화      | 장비와 센서 상태를 파일에 저장하고 객체로 복원                               | `save_devices()`, `load_devices()`                            |
| 13 | `unit13_testing_final_refactor`  | `pytest`, 경계값, 예외 테스트, 최종 구조          | 전체 기능을 테스트하고 패키지 구조를 최종 정리                               | `tests/`, 최종 `device_twin` 패키지                                |


## daily lesson note template
# Day 0

## 오늘의 목표

- 

## 구현할 함수 목록 

- 


## 핵심 개념

- 

## 발견한 문제

- 

## 오늘의 결론


