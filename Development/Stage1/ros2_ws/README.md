# ROS2 adapter — 신규 DDS 실행 미검증
ROS2 Jazzy/rclpy/std_msgs/colcon이 준비된 별도 개발 환경에서 실행한다. 실제 로봇 장치에 연결하지 않는다. 동일 호스트에서만 monotonic timestamp 비교가 유효하다. 아래 명령은 이번 환경에서 실행하지 않았다.

```bash
source /opt/ros/jazzy/setup.bash
colcon build --packages-select lumira_contract_demo
source install/setup.bash
export ROS_DOMAIN_ID=67
export ROS_LOCALHOST_ONLY=1
ros2 run lumira_contract_demo subscriber
```
두 번째 터미널에서도 같은 setup/domain/localhost 설정 후:
```bash
ros2 run lumira_contract_demo publisher
```
publisher는 subscriber discovery 후 20 cycle을 발행하며 종료는 Ctrl-C. 이번 프로세스 간 TCP fixture와 달리 DDS는 cross-topic 순서가 보장되지 않으므로 gesture가 safety보다 먼저 도착하면 거절되는 것이 정상이다. publisher 종료 후 safety sample이 오래되면 gesture 거절 여부를 확인한다. QoS와 late join, process restart/session rollover, malformed/NaN/중복 fixture 시험을 별도 추가한다. 이 adapter는 개발 예시이며 실제 driver/ARM authority/인증/스케줄링은 구현하지 않는다.

일반 로그는 원문 대화·영상·secret을 포함하지 않는다. 기존 /ker/sim의 joint-v1과 다른 /ker/sim/sprint1 namespace를 유지한다. 실기 네임스페이스로 remap하지 않는다.
