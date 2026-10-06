# KR1-1103 ROS 2 노드·토픽 계약 v0.1

작성일: 2026-10-06 KST | Lumira KR1 Sprint1 | 수행: AI 설계·개발 초안

## 결과와 실행 구분
이번 패키지는 /ker/sim/sprint1 전용 개발 모의 통신이다. 기존 /ker/sim joint-v1 패키지와 별도 namespace/schema로 구분하며 기존 0.5초 예시값을 수정하지 않는다. 실기 driver/USB motor 명령은 없다.
이번 실행환경 Ubuntu 24.04에는 ros2/rclpy/docker가 없고 apt ROS 패키지 설정도 없다. 따라서 Python publisher/subscriber 프로세스 간 localhost TCP 전달·계약 검증 로그를 신규 생성하고 ROS 2 rclpy adapter/패키지를 제공한다. 이 로그는 DDS 실행 로그가 아니다.
기존 KR1-248에는 2026-10-04 ROS2 Jazzy CI 3개 transport 시험 통과 기록이 있으나 이는 과거 별도 버전 증적이고 이번 패키지 재시험 결과가 아니다.

|노드|담당 입력|담당 출력|
|---|---|---|
|dialogue_adapter|발화/대화 응답/취소|dialogue_event, gesture_request|
|expression_manager|dialogue_event|expression_state|
|motion_planner|gesture_request|joint_request (후속 실기 adapter 필요)|
|mcu_bridge|USB 상태·안전 입력|joint_states, safety_state|
|power_supervisor|충전·전압·차단 feedback|safety_state 권위 소스와 통합 (중복 publisher 금지)|
|sprint1_publisher/subscriber|합성 fixture|계약 검증 로그만; 하드웨어 출력 없음|

## 토픽 계약
모든 이름 앞에 /ker/sim/sprint1을 붙인다. v0.1 transport는 std_msgs/String 안의 엄격한 JSON, production typed msg/action 전환은 후속. 각 payload 예시는 contract.json/fixtures.jsonl에 저장.

|토픽 suffix|방향|내용|주기 목표|QoS 초안|
|---|---|---|---|---|
|dialogue_event|대화→표정/로그|type, request_id; 원문 제외|이벤트|reliable / volatile / depth10|
|expression_state|표정→화면|state, intensity|변경+5Hz|reliable / volatile / depth1|
|gesture_request|대화→planner|gesture, amplitude|이벤트; 반복은50Hz 이하|reliable / volatile / depth1|
|joint_states|MCU→UI/진단|9개 names, position_rad|20Hz 목표|best_effort / volatile / depth5|
|safety_state|단일 bridge→전체|estop, charging, sensors_valid, armed|변경 즉시+20Hz|reliable / transient_local / depth1|

전송 공통: schema=sprint1-v0.1, session, seq, sent_monotonic_ns, ttl_ms, topic, payload. 모의 fixture는 같은 호스트 clock만 사용. TTL200ms, safety stale100ms는 모의 시험값이며 물리 정지 보장값이 아니다. ROS lifespan/deadline 옵션만으로 안전을 보장하지 않으며 앱 stale 판정과 MCU watchdog이 별도 필요.
구동 명령은 durable 재생 금지. safety_state retained sample도 age 검사하고 publisher 재시작 시 새 session으로 DISARM. 여러 세션 발행을 자동 신뢰하지 않음; transport 인증/SROS2는 후속.

## 거절·상태 규칙
schema/미등록 topic/필드 누락·추가/불리언을 숫자로 사용/NaN/Infinity/크기 초과/오래된 시각/미래 시각/seq 재사용/다른 session을 거절. safety unknown/stale, estop, charging, disarmed면 gesture를 거절. emergency 상태 해제 후에도 자동 armed 금지. 모의 validator는 물리 비상정지를 구현하지 않는다.

## 재현
Python: python3 mock_transport.py → evidence/mock_transport.jsonl + mock_summary.json. Unit: python3 -m unittest discover -s tests -v. ROS2: ros2_ws의 README 절차로 colcon build 후 별도 두 터미널에서 subscriber와 publisher 실행. 기존 namespace에 remap 금지. source hash와 환경 기록 포함.

## AI 검토 의견 / 완료 판정
통신 계약·필드 검증·신규 Python transport 증적 작성. ROS2 adapter는 구문 검사만 가능; 신규 DDS QoS matching/재시작/지연·stop ACK/보드 시험은 미수행. 기존CI 및 신규 Python 결과를 합쳐 실기 성공으로 해석하지 않음. R3 계약 리뷰·DDS 재실행 후 완료 판정. 실제 리뷰어 서명 없음.
공식 QoS 참고: https://design.ros2.org/articles/qos.html , https://github.com/ros2/ros2_documentation/blob/rolling/source/ROS-Framework/interfaces/topics/About-Quality-of-Service-Settings.rst
