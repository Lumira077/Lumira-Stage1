# [F2034] 배터리·충전·전원 관리

Jira: https://lumira077.atlassian.net/browse/KR1-267

BMS·충전·전원 상태를 감시해 저전력/정지·안전 종료 요청을 조정하고 위험 시 실제 보호 회로와 연동한다.

battery chemistry/cell count/BMS spec·SOC 0..1·voltage/current sign/temperature·charger/state·BMS freshness/health·rail/brownout·policy version·shutdown/charge ACK.

actual BMS/charger/PMIC → power state proposal → F2032 motion gate/F2035 diagnostics·OS shutdown handshake. 실제 charge switching/protection은 BMS/회로와 별도.

## 단계별 개발
- 배터리/BMS/충전기/rail·전류부호/단위·low/critical/thermal/overcurrent·brownout·shutdown ordering·charge interlock와 Simulation을 정의한다.
- PowerPolicy는 supplied SOC/temp/current/charging/BMS freshness로 normal/charging/low_power/shutdown_requested/fault/unknown proposal을 생성한다. hardware_action=None·charge_requested=false다.
- 실제 BMS/charger/PMIC·저전압/급차단/과전류/온도·충전중 모션·OS flush/shutdown/정전·통신단절·배터리 runtime을 검증한다.
- 실환경 전원/충전 cycle·조건별 runtime·threshold/calibration freeze·충전/저장/교체·복구 절차와 검토 증적을 확정한다.

## 검증·제한

SOC/voltage/current/temp 정확도·runtime/소비전력·brownout·충전 interlock·fault/stop/shutdown ACK p95

실제 BMS/charger/voltage/cell balance·보호회로·SOC estimation/hysteresis·OS shutdown/charge driver 미연결. 제안 상태는 실제 배터리 보호·충전 완료·안전 종료를 보장하지 않는다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [sensor_msgs BatteryState 계약](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/BatteryState.msg) — 후속 후보; 미설치/미연결.
