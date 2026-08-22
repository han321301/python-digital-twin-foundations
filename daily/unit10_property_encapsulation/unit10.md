# Day 10

## 오늘의 목표

- 객체의 상태를 안전하게 공개하는 클래스 인터페이스를 설계
  
## 구현할 함수 목록 

- def measurements()
- def latest_value()
- def measurement_count()


## 핵심 개념

1. 캡슐화: 객체의 상태를 어떤 방식으로 읽고 변경할 수 있는지 객제를 통제하는 것
   - `sensor.measurements.append(32.5)` -> `sensor.add_measurement(32.5)`
   - 객체가 직접 메서드를 관리하는 방식으로 검증 규칙을 적용할 수 있다 
2. _attribute : '_'을 앞에 붙여서 클래스 내부에서 사용하는 값임을 표현
3. `@property` : 외부에서는 일반 속성처럼 읽히는데, 내부에서는 메서드처럼 동작하게함. 
   - 외부에서 직접 변경하면 안되는 값, 단순 조회 성격의 값, 현재 상태에서 계산되는 값
4. 안전하게 리스트를 반환하기 `tuple(self._measurements)`
5. `setter` 로 쓰기 통제 
  

## 발견한 문제

- 

## 오늘의 결론