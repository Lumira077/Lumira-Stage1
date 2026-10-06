# F2029-S04

Jira: https://lumira077.atlassian.net/browse/KR1-235

대기/깨우기/개인정보·집 내부 배치 비저장·scene 접근·운영 drift/재연결/rollback을 검토한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: person precision/recall·false wake/leave·distance/bearing error·coverage/unknown·p95·센서 장애 복구·민감 scene 노출 0건

제한: 실제 detector/카메라/depth/proximity·object/scene/위험 인지·접근 방향/거리·driver/대기 mode event 미구현. 사람 score gate는 obstacle clearance나 지도/SLAM이 아니다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
