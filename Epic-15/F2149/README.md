# [F2149] Scene 자동화·공간 위치 기반 제어

Jira: https://lumira077.atlassian.net/browse/KR1-706

Scene의 시간/방/사용자/권한 조건·순차 실행·partial failure를 구성

입력/출력: scene id·steps·conditions·cancel·result

경계시험: 일부기기 실패·권한철회·위치변경·중복 trigger

지표: scene 성공률·취소·복구 안내

구현 범위: partial_offline_utility; 공통 utility: scene_proposal. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-15/F2149/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

Stage2 공간/IoT onboarding → 승인 intent/Scene → Stage3 이동조작 → Stage4 높이/전도/접근성/장기 임무. Epic-07 지도·Epic-08 조작·Epic-11 앱·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 승인 IoT device/fabric·Gateway 계정·실제 승강기구/하중/CoM·support polygon·공간지도/권한·장기시험·안전한 작업범위

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
