# [F2031] 메인 컴퓨팅 보드 추상화

Jira: https://lumira077.atlassian.net/browse/KR1-252

RK3588·Jetson·Mini PC 등 보드 교체 시 상위 모듈을 유지하도록 capability·driver·상태/오류를 추상화한다.

board id/arch/OS/ROS distro·CPU/RAM/GPU/NPU·driver/bus/device mapping·capability/version·boot/health·lifecycle/state·resource/temp/power.

BoardProfile → capability check/lifecycle → actual camera/mic/joint/BMS/display driver adapters. 현재 mock/x86_64/aarch64 profile만 허용한다.

## 단계별 개발
- target 보드/OS/driver·UART/CAN/I2C/SPI/USB·device 권한·capability·version·mock/hardware 분리와 교체 Simulation을 설계한다.
- BoardHAL의 profile/arch/capability 검증·configure/activate/deactivate/error/cleanup·복사 격리를 구현한다. 실제 SDK/driver는 후속이다.
- 실제 보드 교체·device missing/reset/permission·resource/NPU provider·hotplug/boot·HAL 성능/thermal·상위 모듈 호환을 검증한다.
- 실환경 장시간/재부팅·BOM/OS/SDK/driver freeze·calibration·복구/rollback과 유지보수 기준을 확정한다.

## 검증·제한

보드 교체 계약 호환·boot/driver recovery·CPU/RAM/GPU/NPU/온도·bus latency·device fault isolation

실제 RK3588/Jetson SDK/OS/device discovery/driver/NPU·장시간 실기 미연결. arch capability fixture는 실제 보드 지원/성능을 입증하지 않는다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ros2_control Hardware Component](https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/writing_new_hardware_component.html) — 후속 후보; 미설치/미연결.
