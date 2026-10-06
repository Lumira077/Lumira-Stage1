# F2031-S03

Jira: https://lumira077.atlassian.net/browse/KR1-255

실제 보드 교체·device missing/reset/permission·resource/NPU provider·hotplug/boot·HAL 성능/thermal·상위 모듈 호환을 검증한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: 보드 교체 계약 호환·boot/driver recovery·CPU/RAM/GPU/NPU/온도·bus latency·device fault isolation

제한: 실제 RK3588/Jetson SDK/OS/device discovery/driver/NPU·장시간 실기 미연결. arch capability fixture는 실제 보드 지원/성능을 입증하지 않는다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
