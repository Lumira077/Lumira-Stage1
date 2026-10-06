# [F2084] 가사 작업 계획

Jira: https://lumira077.atlassian.net/browse/KR1-666

가사 요청을 자원/안전 precondition·navigation/manipulation 단계로 분해

입력/출력: task DAG·resources·preconditions·cancel epoch

경계시험: 불가능 작업·partial failure·열/날카로운 물체

지표: 완료율·재계획·미승인 작업 0건

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-15/F2084/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

Stage2 공간/IoT onboarding → 승인 intent/Scene → Stage3 이동조작 → Stage4 높이/전도/접근성/장기 임무. Epic-07 지도·Epic-08 조작·Epic-11 앱·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 승인 IoT device/fabric·Gateway 계정·실제 승강기구/하중/CoM·support polygon·공간지도/권한·장기시험·안전한 작업범위

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
