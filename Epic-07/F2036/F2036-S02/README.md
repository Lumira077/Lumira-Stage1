# [F2036-S02] LiDAR·Depth·Odometry 센서 융합 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-285

ROS2/제어/센서·actuator adapter 구현 및 version 관리: LiDAR·Depth·IMU·Wheel odometry를 공통 시각/TF로 보정하고 covariance 기반 fusion 입력을 구성

데이터: scan/pointcloud/imu/odom·stamp·frame·calibration

검증: clock reset·센서 누락·wheel slip·outlier

지표: timestamp skew·pose drift·invalid 비율

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
