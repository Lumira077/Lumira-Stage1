# F2022-S01

Jira: https://lumira077.atlassian.net/browse/KR1-181

실제 URDF/관절 mapping·home/calibration·가동/속도/가감속/jerk·충돌/끼임/thermal·stop 경로·gesture version 계약을 정의한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: tracking error·position/velocity/acceleration/jerk limits·실제 clearance/접촉·stop latency·전류/온도·failure recovery

제한: provisional limits이며 실제 URDF/모터/feedback/충돌·끼임 감지·가감속/jerk/watchdog/E-stop controller 미연결. start pose 불일치는 거절하며 실제 복귀 trajectory를 계산하지 않는다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
