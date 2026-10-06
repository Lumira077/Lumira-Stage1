# F2032-S02

Jira: https://lumira077.atlassian.net/browse/KR1-259

MockMotor의 bounded target/step·명령시간 역행·software watchdog·latched stop 및 ACK/healthy fixture reset을 구현한다. 실제 bus/PWM/torque 제어는 후속이다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 ROS2/HAL/센서/제어 adapter 및 재현 버전, S03 실제 장비의 제어/센서/전원 품질·통합/성능/안전 증적, S04 실환경 임무 검증·Parameter Freeze·rollback·Q1/R1 증적 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: tracking error·제어 jitter·position/velocity/acceleration/jerk·전류/온도·watchdog/정지시간·실제 stop ACK·reset evidence

제한: 실제 motor/servo/CAN/PWM/encoder·다관절/effort/가감속/jerk/collision·hardware E-stop/watchdog·물리 정지/안전자세 미연결. software latch/Mock position은 실제 모터 안전 제어가 아니다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
