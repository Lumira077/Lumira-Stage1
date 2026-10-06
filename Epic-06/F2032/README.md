# [F2032] 관절 및 서보 모터 제어

Jira: https://lumira077.atlassian.net/browse/KR1-257

목·팔·허리·손 관절을 measured-state/한계/속도·안전 우선순위로 제어하고 정지/고장/통신 단절을 처리한다.

URDF/joint map·radian measured position/velocity/effort·command timestamp/seq·calibration/home·position/velocity/acceleration/jerk/current/temp·stop latch/operator reset/watchdog·feedback ACK.

Epic-04 gesture/Epic-05 head proposal → validation/safety/ros2_control FollowJointTrajectory → actual actuator driver/encoder feedback. 현 MockMotor는 한 joint의 메모리 position만 갱신한다.

## 단계별 개발
- 실제 관절/서보 mapping·단위/극성/home/calibration·position/속도/가감속/jerk·충돌/끼임/thermal·E-stop/watchdog·reset 계약을 설계한다.
- MockMotor의 bounded target/step·명령시간 역행·software watchdog·latched stop 및 ACK/healthy fixture reset을 구현한다. 실제 bus/PWM/torque 제어는 후속이다.
- 실제 encoder/tracking·multi-joint·position/속도/가감속/jerk·충돌/접촉·전류/온도·stale/통신단절/stop latency·무자동재시작을 검증한다.
- 실환경 임무/정지·안전자세·원점/유지보수·URDF/limits/calibration/제어 parameter freeze·rollback 증적을 확정한다.

## 검증·제한

tracking error·제어 jitter·position/velocity/acceleration/jerk·전류/온도·watchdog/정지시간·실제 stop ACK·reset evidence

실제 motor/servo/CAN/PWM/encoder·다관절/effort/가감속/jerk/collision·hardware E-stop/watchdog·물리 정지/안전자세 미연결. software latch/Mock position은 실제 모터 안전 제어가 아니다.

S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-06/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 카메라/인식 모델/센서/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/epoch/quality/live/VAD/echo를 공급한다; 실제 인증·동의·센서/분류 서비스가 아니다.

도구 참조: [ros2_control Hardware Component](https://control.ros.org/jazzy/doc/ros2_control/hardware_interface/doc/writing_new_hardware_component.html) — 후속 후보; 미설치/미연결.
