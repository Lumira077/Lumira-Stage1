# F2034-S03

Jira: https://lumira077.atlassian.net/browse/KR1-270

실제 BMS/charger/PMIC·저전압/급차단/과전류/온도·충전중 모션·OS flush/shutdown/정전·통신단절·배터리 runtime을 검증한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: SOC/voltage/current/temp 정확도·runtime/소비전력·brownout·충전 interlock·fault/stop/shutdown ACK p95

제한: 실제 BMS/charger/voltage/cell balance·보호회로·SOC estimation/hysteresis·OS shutdown/charge driver 미연결. 제안 상태는 실제 배터리 보호·충전 완료·안전 종료를 보장하지 않는다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
