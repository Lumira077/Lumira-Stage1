# [F2045] 안전 파지 및 놓기

Jira: https://lumira077.atlassian.net/browse/KR1-334

접근→접촉→파지→운반→지지면 확인→놓기 상태를 구성

입력/출력: grasp pose·force·support·feedback·object id

경계시험: slip·과압·지지면 없음·전원 단절

지표: 파지/놓기 성공률·파손/낙하 0건

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-08/F2045/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

팔/손 HW·물체 pose → 파지/force/slip → 한손/양손·협조 → 심부름. Epic-05 인지·Epic-06 제어·Epic-07 이동·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 실제 양팔/5-Finger·URDF/SRDF·joint mapping/encoder·손끝 calibration·허용하중/힘·시험물체·독립 E-stop·안전 지지면

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
