# Day 02: 딕셔너리와 자료구조 설계

## 오늘의 목표

- 데이터를 어떤 구조로 저장해야 조회·추가·수정·삭제가 명확해지는지 판단한다.

## 구현할 함수 목록 

- register_device
- find_device
- register_sensor
- remove_sensor
- list_sensor_ids

## 핵심 개념

- 조회: [], in, get()
- setdefault()
- hash()
- del, pop()

## 발견한 문제

- 딕셔너리 하위 키에 바로 접근하려고 할 때, 상위 키가 없으면 KeyError가 발생함 
- setdefault()의 동작 방식을 정확히 구분하지 않고 뒤에 바로 .append()를 붙이면 에러가 날 수 있음


## 오늘의 결론

딕셔너리의 빠른 탐색 속도와 setdefault()를 활용한 안전한 중첩 데이터 처리의 자료구조 설계 이해
