# Python Digital Twin Learning Curriculum

## 학습 목표

Python 핵심 개념을 하나의 장비·센서 상태 관리 예제에 계속 적용하면서 익히고, 이후 FastAPI + DB + 비동기 센서 처리까지 연결한다.

- Python의 객체·함수·자료구조 동작 원리를 이해한다.
- 하나의 디지털트윈 예제를 확장하면서 개념을 연결한다.
- 새 기술이나 라이브러리가 등장할 때 사용법뿐 아니라 왜 필요한지 이해한다.
- Python 중급 개념을 실제 백엔드 구조와 연결한다.
- 최종적으로 센서 데이터를 수집·검증·저장·조회하는 비동기 API 구조를 이해한다.

---

## 전체 커리큘럼

| 단계 | 폴더명 | 핵심 내용 | 주요 Python / Backend 개념 |
|---:|---|---|---|
| 01 | `day01_object_reference` | 객체, 참조, 가변성, 복사 | 객체와 이름, `is` / `==`, mutable / immutable, shallow/deep copy |
| 02 | `day02_dictionary_design` | 딕셔너리와 자료구조 설계 | `dict`, 중첩 자료구조, 키 조회, 자료구조 선택 |
| 03 | `day03_function_design` | 함수 설계와 부작용 | 인자, 반환값, 기본 인자, 부작용, 타입 힌트 |
| 04 | `unit04_class_instance` | 클래스와 인스턴스 | `class`, `self`, `__init__`, 인스턴스/클래스 속성 |
| 05 | `unit05_iteration_comprehension` | 반복 처리와 컴프리헨션 | `for`, comprehension, `any()`, `all()`, `enumerate()` |
| 06 | `unit06_sort_group_latest` | 정렬, 그룹화, 최신 상태 | `sorted()`, `key`, `lambda`, `min/max`, 그룹화 |
| 07 | `unit07_module_refactoring` | 모듈 분리와 리팩터링 | `import`, 모듈 경계, 실행 진입점, 책임 분리 |
| 08 | `unit08_exception_contract` | 예외 처리와 실패 계약 | `try/except`, `raise`, 사용자 정의 예외, 예외 전파 |
| 09 | `unit09_dataclass_composition` | 데이터 클래스와 객체 합성 | `dataclass`, `field`, `default_factory`, composition |
| 10 | `unit10_property_encapsulation` | 프로퍼티와 캡슐화 | `@property`, 내부 상태, 방어적 복사, 캡슐화 |
| 11 | `unit11_iterator_generator` | 반복자와 제너레이터 | iterable, iterator, `iter()`, `next()`, `yield` |
| 12 | `unit12_api_serialization` | 파일·JSON·직렬화 | `json`, `pathlib`, `with`, serialization |
| 13 | `unit13_function_objects` | 함수 객체와 고차 함수 | 함수도 객체, 함수를 인자로 전달, 함수를 반환, 함수 매핑 |
| 14 | `unit14_decorator` | 데코레이터 | wrapper, decorator, `functools.wraps`, 공통 로직 분리 |
| 15 | `unit15_fastapi_basics` | FastAPI 기초 | HTTP 요청/응답, route, GET/POST, path parameter, Pydantic |
| 16 | `unit16_sensor_stream_collections` | 센서 스트림과 `collections` | generator 심화, `deque`, `defaultdict`, `Counter` |
| 17 | `unit17_typing_protocol` | 타입 힌트와 인터페이스 | `Optional`, type alias, `Protocol`, 구조적 타이핑 |
| 18 | `unit18_database_crud` | DB 기초와 CRUD | DB 연결, 모델/테이블, insert/select/update/delete, Repository 연결 |
| 19 | `unit19_pytest_mock` | 테스트 심화 | fixture, 예외 테스트, mock, patch, 외부 의존성 격리 |
| 20 | `unit20_async_await` | async/await 기초 | coroutine, `async`, `await`, event loop, 비동기 I/O |
| 21 | `unit21_async_sensor_pipeline` | 비동기 센서 파이프라인 통합 | `asyncio.gather()`, 동시 센서 수집, DB 저장, FastAPI 조회 |

---

## lesson note template

# Unit

## 오늘의 목표

- 

## 구현할 함수 목록 

- 


## 핵심 개념

- 

## 발견한 문제

- 

## 오늘의 결론
