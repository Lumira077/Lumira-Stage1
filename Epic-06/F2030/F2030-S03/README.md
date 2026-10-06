# F2030-S03

Jira: https://lumira077.atlassian.net/browse/KR1-250

실제 DDS QoS/재전송/늦은 명령·restart/cancel·typed interface·clock reset·deadline/liveliness·node fault/네트워크·SROS2를 통합 시험한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: topic/action end-to-end p50/p95·deadline/liveliness/jitter·lost/late/duplicate·startup recovery·cancel/stop ACK·허용 외 command 0건

제한: production typed interface·TF/lifecycle supervisor/SROS2·실제 제어주기/실기·DDS network fault/real-time 검증 미완료. ROS Node는 /ker/sim Mock 전용이며 String JSON은 개발용 transport 계약이다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
