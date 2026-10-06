# F2120-S03

Jira: https://lumira077.atlassian.net/browse/KR1-280

실제 local/NPU/GPU/Cloud 실행·resource saturation/deadline·provider 장애·fallback/retry/idempotency·취소/usage·원문 미전송을 통합 시험한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: queue/end-to-end deadline·CPU/RAM/GPU/NPU·route/fallback latency·cost/usage·취소/stale result·제어 Cloud placement 0건·민감 전송 0건

제한: actual Provider/NPU/resource probe·latency/cost model·우선순위/timeout/retry/fallback adapter·owner/auth/자동동의 event 미구현. 실제 호출 0이며 budget은 fixture다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
