# F2127-S02

Jira: https://lumira077.atlassian.net/browse/KR1-238

현재 SpeakerAssociator는 supplied DOA와 visual bearing의 circular angle·freshness/skew/quality/epoch·20도 후보 cone·10도 ambiguity margin 및 VAD/echo gate를 구현한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: active speaker precision/recall·ID switch·TV/echo 오탐·획득/전환/재획득 p95·DOA/vision angular error·time skew/unknown

제한: 실제 DOA/VAD/AEC·head 획득·camera tracker/립 활동·지속 추적 상태/전환 hysteresis·auth/epoch event 미연결. 방향 일치는 실제 화자 확정/사용자 인증이 아니며 TV source를 자동 검출하지 않는다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
