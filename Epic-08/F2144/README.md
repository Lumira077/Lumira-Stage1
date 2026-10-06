# [F2144] Force·Slip 기반 Adaptive Soft Grasp

Jira: https://lumira077.atlassian.net/browse/KR1-359

force/slip feedback로 힘 증분·재파지·중단을 결정

입력/출력: force·slip·max force·force rate·feedback age

경계시험: 계속 slip·과압·센서 stale·파손 위험

지표: slip 회복률·힘 overshoot·낙하/파손

구현 범위: partial_offline_utility; 공통 utility: grasp_proposal. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-08/F2144/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

팔/손 HW·물체 pose → 파지/force/slip → 한손/양손·협조 → 심부름. Epic-05 인지·Epic-06 제어·Epic-07 이동·Epic-13 안전·Epic-16 HW 연결.

필요 입력/연동: 실제 양팔/5-Finger·URDF/SRDF·joint mapping/encoder·손끝 calibration·허용하중/힘·시험물체·독립 E-stop·안전 지지면

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
