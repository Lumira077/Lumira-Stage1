# EPIC-07 Stage 2 실내 자율주행

https://lumira077.atlassian.net/browse/KR1-282

7 Features, 28 existing Sub-tasks.

센서/TF → 지도/위치 → 경로/장애물 → 도킹 → 공간 Wizard. Epic-06 코어·Epic-16 HW·Epic-13 독립 안전·Epic-11 앱·Epic-15 공간과 연결.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2036] LiDAR·Depth·Odometry 센서 융합](F2036/README.md): LiDAR·Depth·IMU·Wheel odometry를 공통 시각/TF로 보정하고 covariance 기반 fusion 입력을 구성
- [[F2037] 실내 지도 작성(SLAM)](F2037/README.md): SLAM pose graph·loop closure·OccupancyGrid 저장/복구와 지도 revision을 관리
- [[F2038] 자기 위치 추정](F2038/README.md): map 기반 pose/covariance를 추정하고 위치 상실·kidnapped robot 재초기화를 처리
- [[F2039] 목적지 경로 계획 및 추종](F2039/README.md): 목적지/금지구역을 검증하고 global/local 경로 및 취소·재계획을 연결
- [[F2040] 동적 장애물 회피](F2040/README.md): 사람/반려동물/가구/낙하위험의 costmap 반영과 안전한 감속·정지를 처리
- [[F2041] 자동 복귀 및 무선 충전 도킹](F2041/README.md): 저전력 복귀·dock 탐색/정렬·충전 확인·횟수 제한 재시도를 상태기로 구성
- [[F2152] Network·SLAM Mapping·방 이름 설정 Wizard](F2152/README.md): 연결→지도 작성→방 이름/금지구역→저장·재개 Wizard를 구성
