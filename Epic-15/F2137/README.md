# [F2137] Stage4 가변 높이 범위·승강 Mechanism

Jira: https://lumira077.atlassian.net/browse/KR1-686

700~1200mm 구상 목표의 승강·limit·position·구조를 설계 검증

입력/출력: stroke·height·load·drawing·limit·calibration

경계시험: 끼임·중간전원단절·기울기·과부하

지표: 강성·위치오차·승강수명·정지

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-15/F2137/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

Stage2 공간/IoT onboarding → 승인 intent/Scene → Stage3 이동조작 → Stage4 높이/전도/접근성/장기 임무. Epic-07 지도·Epic-08 조작·Epic-11 앱·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 승인 IoT device/fabric·Gateway 계정·실제 승강기구/하중/CoM·support polygon·공간지도/권한·장기시험·안전한 작업범위

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
