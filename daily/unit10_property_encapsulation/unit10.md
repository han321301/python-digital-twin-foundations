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
2. _attribute : '_'을 앞에 붙여서 클래스 내부에서 사용하는 값임을 표현
3. `@property`
   - 외부에서는 일반 속성처럼 읽히는데, 내부에서는 메서드처럼 동작하게함. 
   - `@property`로 리턴하더라도, 리스트, 딕셔너리, 세트와 같은 가변(Mutable) 객체값은 리스트 메서드(append 등)를 통해 외부에서 값 변경이 가능함. tuple(list)로 차단 가능
4. `setter`는 쓰기 통제하고, 별도 선언없이 변수가 생성

## 발견한 문제

- `_measurements[-1] or None` => `_measurements[-1:] or None` 

## 오늘의 결론

- `@property` 핵심 목적
  - 1. 데이터 보호 및 읽기 전용(Read-Only) 구현 (가변 객체는 `tuple()`)
  - 2. setter로 올바른 데이터만 입력받기 (유효성 검사) 
  - 3. 실시간 계산된 값 제공 `latest_value`

## 질문
- sensor_id가 함수 버튼이 되면, 상자로서는 초기값만 가져와서 방치되는 것? 
- setter 안에서 그 초기값이 저장된 매개변수에 값을 저장해서 쓰면 무한 루프가 돈다?
