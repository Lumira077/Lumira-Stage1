# F2023-S04

Jira: https://lumira077.atlassian.net/browse/KR1-189

사용자 자연성·동기 어긋남/끼어들기 평가·큐 원문 비저장·rollback·장애 후 기본표정/물리 정지 정책을 검토한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: face/audio/motion onset/skew/drift p50/p95·late/drop·취소 요청→ACK/물리정지·잔여출력·clock reversal

제한: actual clock/renderer/audio/motor adapter·ACK timeout/watchdog·자동 동의/사용자 전환 이벤트 전파 미구현. 가상 ACK는 물리 정지 증거가 아니다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
