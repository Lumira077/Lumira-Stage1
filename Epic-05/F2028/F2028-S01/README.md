# F2028-S01

Jira: https://lumira077.atlassian.net/browse/KR1-227

센서 region/전기 입력·단위/calibration·tap/long/double·debounce/stuck·동시 입력/순서/복구·사용자/epoch 계약을 설계한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: tap/long 오탐/누락·중복 이벤트·debounce/release p95·고착/재연결·region 혼선·사용자 접근성

제한: 실제 touch driver/sensor calibration·double-tap/pressure·contact watchdog/즉시 long 이벤트·자동 사용자/철회 event 미연결. release 기반 Prototype은 고착 중 자동 알림/정지를 구현하지 않는다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
