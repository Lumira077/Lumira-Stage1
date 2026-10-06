# F2027-S04

Jira: https://lumira077.atlassian.net/browse/KR1-225

사용자/문화/연령별 제스처 이해·오작동·접근성·대체 터치/음성 입력과 모델/정책 rollback을 확인한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: gesture macro-F1/confusion matrix·pose angle error·거리/조명/가림 coverage·중복 이벤트·FAR/누락·p95 latency

제한: 실제 MediaPipe/카메라/landmark/gesture classifier·track/자동 epoch event·stop controller·사용자 평가 없음. supplied stop tag는 safety_estop=false/executable=false이다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
