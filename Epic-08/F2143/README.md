# [F2143] 물체 재질·취약성 추정 및 Unknown 안전정책

Jira: https://lumira077.atlassian.net/browse/KR1-354

vision/접촉으로 재질·취약성을 추정하고 Unknown일 때 보수적인 파지 정책을 적용

입력/출력: material·fragility·confidence·approved force

경계시험: 유리/도자기/연질·충돌 정보·낮은 신뢰

지표: 재질 분류·Unknown 거절·파손 0건

구현 범위: partial_offline_utility; 공통 utility: grasp_proposal. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-08/F2143/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

팔/손 HW·물체 pose → 파지/force/slip → 한손/양손·협조 → 심부름. Epic-05 인지·Epic-06 제어·Epic-07 이동·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 실제 양팔/5-Finger·URDF/SRDF·joint mapping/encoder·손끝 calibration·허용하중/힘·시험물체·독립 E-stop·안전 지지면

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
