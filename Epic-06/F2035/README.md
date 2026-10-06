# [F2035] 로봇 자가진단 및 장애 코드

Jira: https://lumira077.atlassian.net/browse/KR1-272

장치 heartbeat·오류코드·고장 격리와 검토된 복귀를 통합해 서비스/운영에 상태를 제공한다.

device/source/version·heartbeat time·severity/code/latched state·bounded error metadata·operator/healthy evidence·hardware watchdog·fault isolation/recovery ACK·privacy.

HAL/motor/sensor/power·resource telemetry → DiagnosticArray·bounded fault registry → safety controller/운영 모니터링. 현재 소프트웨어 report이며 실제 hardware watchdog/복귀 실행 없음.

## 단계별 개발
- fault code/severity·heartbeat/timeout·latch/isolation/recovery·boot self-test·비저장 로그/보존·Simulation fault injection을 정의한다.
- Diagnostics는 allowlist E_COMM/E_THERMAL/E_POWER/E_STOP·bounded heartbeat/fault registry·freshness·operator/healthy fixture clear·hardware_stop_confirmed=false를 구현한다.
- 실제 driver·HW watchdog·장치 단절/고착/발열·fault injection·격리/동작 차단/재연결·운영 telemetry·민감 로그 차단을 검증한다.
- 실환경 임무/장시간 고장·오류코드/threshold/복귀 parameter freeze·사용자 안내/유지보수·운영 rollback 증적을 확정한다.

## 검증·제한

fault detection/격리/복귀 p95·heartbeat stale·오류코드 coverage·실제 stop/healthy ACK·fault recurrence·민감 로그 0건

실제 device self-test/현재온도·hardware watchdog·severity escalation/고장 격리 actuator·fleet telemetry 미연결. bounded software heartbeat/fault code는 실제 안전장치 인증이 아니다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ROS2 diagnostics](https://github.com/ros/diagnostics) — 후속 후보; 미설치/미연결.
