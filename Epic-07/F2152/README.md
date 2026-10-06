# [F2152] Network·SLAM Mapping·방 이름 설정 Wizard

Jira: https://lumira077.atlassian.net/browse/KR1-313

연결→지도 작성→방 이름/금지구역→저장·재개 Wizard를 구성

입력/출력: network ref·map revision·room id·zone·step

경계시험: 불완전지도·가구변경·네트워크 끊김·중복 방 이름

지표: 온보딩 완료율·재개 일관성·설정 보존

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-07/F2152/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

센서/TF → 지도/위치 → 경로/장애물 → 도킹 → 공간 Wizard. Epic-06 코어·Epic-16 HW·Epic-13 독립 안전·Epic-11 앱·Epic-15 공간과 연결.

필요 입력/연동: 실제 이동베이스·LiDAR/Depth/IMU/encoder·URDF/footprint·TF/clock·승인 속도/정지거리·cliff 센서·dock/BMS·실내 지도·시험 공간

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
