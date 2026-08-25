# Day 11

## 오늘의 목표

- 스트리밍 데이터 처리 파이프라인 이해 

## 구현할 함수 목록 

- read_measurements
- stream_device_alerts


## 핵심 개념

- Iterator: 값을 next()로 하나씩 꺼낼 수 있는 모든 객체 
- Generator: Iterator를 쉽고 간편하게 만들 수 있도록 하는 함수. 함수 안에 yield 키워드를 넣기만 하면 파이썬이 알아서 이터레이터 규칙을 만들어 줌 
- Generator를 for문으로 순차 실행, next()로 하나씩 수동 실행 할 수 있다. 
- 또는 list(), tuple()로 자료형으로 한번에 변환 가능 (메모리 절약 효과 사라짐)

## 발견한 문제

- `limit = threshold[record["sensor_type"]]` 에서 센서 타입이 등록되지 않은 경우 KeyError 발생 
- `limit = threhold.get(record["sensor_type"], 999.0)`

## 오늘의 결론
- 리스트와 제너레이터 쓰임 구분 
  - Generator: 대량 데이터를 한번만 순차 처리할 때, 스트리밍 데이터 
  - List: 결과를 여러번 사용할 예정, 인덱스로 접근해야 할 때 
  