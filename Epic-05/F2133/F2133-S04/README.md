# F2133-S04

Jira: https://lumira077.atlassian.net/browse/KR1-245

응시/머리 움직임 불편·안전 거리·접촉·추적 해제 UX·실제 실패 복구/기본자세·config rollback을 검토한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 인식 모델/센서/제어 adapter 및 재현 버전, S03 실제 장비의 인지/추적 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: face center/angle tracking error·jitter/settling/획득 p95·joint limit/velocity/가감속/jerk·lost/stop/clearance·전류/온도

제한: 실제 head motor/controller/feedback·yaw/pitch calibration·track identity/자동 epoch event·가감속/jerk/collision/watchdog·물리 정지 ACK 미연결. 예시 FOV/gain/limits는 승인 필요이며 hold proposal이 실제 물리 정지를 뜻하지 않는다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
