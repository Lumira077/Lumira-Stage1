# [F2041] 자동 복귀 및 무선 충전 도킹

Jira: https://lumira077.atlassian.net/browse/KR1-308

저전력 복귀·dock 탐색/정렬·충전 확인·횟수 제한 재시도를 상태기로 구성

입력/출력: SOC·dock pose·contact·charge feedback·retry

경계시험: dock 막힘·false contact·BMS fault·재시도 소진

지표: 도킹 성공률·소요시간·충전 실제 ACK

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-07/F2041/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

센서/TF → 지도/위치 → 경로/장애물 → 도킹 → 공간 Wizard. Epic-06 코어·Epic-16 HW·Epic-13 독립 안전·Epic-11 앱·Epic-15 공간과 연결.

필요 입력/연동: 실제 이동베이스·LiDAR/Depth/IMU/encoder·URDF/footprint·TF/clock·승인 속도/정지거리·cliff 센서·dock/BMS·실내 지도·시험 공간

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
