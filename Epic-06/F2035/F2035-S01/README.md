# F2035-S01

Jira: https://lumira077.atlassian.net/browse/KR1-273

fault code/severity·heartbeat/timeout·latch/isolation/recovery·boot self-test·비저장 로그/보존·Simulation fault injection을 정의한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: fault detection/격리/복귀 p95·heartbeat stale·오류코드 coverage·실제 stop/healthy ACK·fault recurrence·민감 로그 0건

제한: 실제 device self-test/현재온도·hardware watchdog·severity escalation/고장 격리 actuator·fleet telemetry 미연결. bounded software heartbeat/fault code는 실제 안전장치 인증이 아니다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
