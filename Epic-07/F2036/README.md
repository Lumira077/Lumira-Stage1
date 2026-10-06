# [F2036] LiDAR·Depth·Odometry 센서 융합

Jira: https://lumira077.atlassian.net/browse/KR1-283

LiDAR·Depth·IMU·Wheel odometry를 공통 시각/TF로 보정하고 covariance 기반 fusion 입력을 구성

입력/출력: scan/pointcloud/imu/odom·stamp·frame·calibration

경계시험: clock reset·센서 누락·wheel slip·outlier

지표: timestamp skew·pose drift·invalid 비율

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-07/F2036/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

센서/TF → 지도/위치 → 경로/장애물 → 도킹 → 공간 Wizard. Epic-06 코어·Epic-16 HW·Epic-13 독립 안전·Epic-11 앱·Epic-15 공간과 연결.

필요 입력/연동: 실제 이동베이스·LiDAR/Depth/IMU/encoder·URDF/footprint·TF/clock·승인 속도/정지거리·cliff 센서·dock/BMS·실내 지도·시험 공간

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
