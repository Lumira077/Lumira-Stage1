# [F2030] ROS2 노드 및 토픽 아키텍처

Jira: https://lumira077.atlassian.net/browse/KR1-247

AI/서비스와 센서/모터/전원/디스플레이를 ROS2 Node·Topic·Service·Action·QoS 계약으로 연결하고 제어·안전 경로를 분리한다.

robot namespace/frame id·schema/version·generation/seq·monotonic deadline·command/feedback·QoS reliability/durability/depth/deadline/liveliness·lifecycle·cancel/stop ACK.

dev /ker/sim/joint_request(std_msgs/String JSON) → CommandGate/MockMotor → /ker/sim/joint_states(sensor_msgs/JointState) 및 /ker/sim/diagnostics(DiagnosticArray). production typed custom msg/action/SROS2·robot namespace·TF는 후속 설계.

## 단계별 개발
- Node graph·topic/service/action·ROS msg/frame/QoS·CPU thread/제어주기·startup/lifecycle·clock/reset·safety priority와 Simulation Case를 정의한다.
- CommandGate의 mock robot/schema·generation/seq/deadline/finite 범위를 구현하고 rclpy simulator Node/launch·ROS2 DDS transport 시험을 작성한다.
- 실제 DDS QoS/재전송/늦은 명령·restart/cancel·typed interface·clock reset·deadline/liveliness·node fault/네트워크·SROS2를 통합 시험한다.
- 실환경 임무·startup/shutdown·지연/jitter·통신/안전·관측성·resource를 검증하고 version/Parameter Freeze·rollback 증적을 확정한다.

## 검증·제한

topic/action end-to-end p50/p95·deadline/liveliness/jitter·lost/late/duplicate·startup recovery·cancel/stop ACK·허용 외 command 0건

production typed interface·TF/lifecycle supervisor/SROS2·실제 제어주기/실기·DDS network fault/real-time 검증 미완료. ROS Node는 /ker/sim Mock 전용이며 String JSON은 개발용 transport 계약이다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ROS2 Jazzy QoS 계약](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Quality-of-Service-Settings.html) — 후속 후보; 미설치/미연결.
