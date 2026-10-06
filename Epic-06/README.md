# EPIC-06 ROS2 로봇 코어 및 하드웨어 제어

Jira: https://lumira077.atlassian.net/browse/KR1-246

7개 Feature(F2030~F2035/F2120), 28개 Sub-task. 첨부 7 Feature/76 SP·AI로봇사업.docx를 기준으로 한다. 현 S04 명칭은 실환경 임무 검증·Parameter Freeze다.

로컬 실행: `python Epic-06/runtime/run.py` / `python Epic-06/runtime/demo.py` (Python3.11+, stdlib).

현재: command generation/seq/deadline·BoardHAL mock lifecycle·한 joint의 메모리 position/속도 bound/watchdog/stop latch·common-clock metadata pair·power policy·heartbeat/fault allowlist·local/edge/cloud placement/결과 취소 계약. 실제 hardware 호출 없음.

ROS2 소스: ros2/ker_core는 ament_python simulator package다. `/ker/sim/joint_request` String JSON → MockMotor → `/ker/sim/joint_states` JointState 및 `/ker/sim/diagnostics` DiagnosticArray; SetBool enable_mock은 개발용 reset/stop만 제공한다. production topic/typed command/actuator driver가 아니며 외부 물리 장치와 연결하지 않는다. timestamp는 동일 host monotonic 기준이다. CI ROS Jazzy DDS 송수신 시험과 Python 합성 계약 시험을 구분한다. actual colcon/보드/real-time·hardware safety는 별도 검증해야 한다.

ROS2 환경에서: `source /opt/ros/jazzy/setup.bash`; `python3 Epic-06/ros2/ker_core/test_ros_transport.py`. 패키지 실행은 `colcon build --base-paths Epic-06/ros2/ker_core` 후 `source install/setup.bash`, `ros2 launch ker_core_sim simulator.launch.py`. 설치/launch 실행은 환경별 별도 검증한다.

실제 RK3588/Jetson SDK/모터/encoder/BMS/PMIC·ros2_control hardware plugin·SROS2/auth·clock calibration·가감속/jerk/충돌/접촉·hardware E-stop/watchdog·물리 stop ACK 미연결. 소프트웨어 Mock 정지는 실제 안전 정지 증거가 아니다. chemistry/BMS/URDF/제어 limits는 fixture/예시를 승인 없이 운영 사용하지 않는다. 원본 대화/영상·비밀값은 일반 로그에 남기지 않는다.

통합 계약: Epic-02 대화/취소/Local-Cloud 정책 → Epic-04 표현·Epic-05 head proposal → ROS2 코어/HAL/안전제어·feedback → diagnostics/전원; 센서 공통 시각은 Epic-03/05 인지에 전달한다. 실제 event bus/adapter·production policy/resources/provider는 추가 개발이다.

S04: source/ROS distro/OS/driver/URDF/calibration/limits/QoS/전원/정책 version·실환경 sample·실제 임무/통신고장/stop/재부팅·Parameter Freeze·Q1/R1·rollback 증적 확보 전 release_ready=false. 7개 Feature의 현 due date는 Epic due 2027-08-31 안에 있으며 Jira 상태/담당자/날짜를 변경하지 않는다.
