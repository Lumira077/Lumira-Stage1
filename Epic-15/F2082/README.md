# [F2082] 높이 조절 본체

Jira: https://lumira077.atlassian.net/browse/KR1-656

Stage4 높이 조절 actuator·absolute position·limit·과부하·끼임 구조를 설계

입력/출력: height·stroke·encoder·limit switch·load

경계시험: 상한/하한·과부하·encoder fault·전원단절

지표: 높이 오차·강성·정지거리·전도 안정성

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-15/F2082/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

Stage2 공간/IoT onboarding → 승인 intent/Scene → Stage3 이동조작 → Stage4 높이/전도/접근성/장기 임무. Epic-07 지도·Epic-08 조작·Epic-11 앱·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 승인 IoT device/fabric·Gateway 계정·실제 승강기구/하중/CoM·support polygon·공간지도/권한·장기시험·안전한 작업범위

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
