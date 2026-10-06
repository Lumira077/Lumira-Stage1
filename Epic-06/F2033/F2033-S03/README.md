# F2033-S03

Jira: https://lumira077.atlassian.net/browse/KR1-265

실제 camera/mic/touch/IMU driver·HW timestamp/offset/drift·frame loss/재연결/queue·sim time reset·노이즈/지연·민감 raw 차단을 검증한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: sensor skew/drift p50/p95·frame loss/stale/queue depth·재연결/reset·단위/좌표 mismatch·개인정보 비저장

제한: actual drivers/PTP/HW clock calibration·raw buffer/message_filters/TF/offset estimation 미구현. supplied common clock을 검증하며 실제 clock synchronization을 완료한 것이 아니다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
