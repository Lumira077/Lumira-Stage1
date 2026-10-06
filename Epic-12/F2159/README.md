# [F2159] Device-Customer Mapping·Lifecycle 관리

Jira: https://lumira077.atlassian.net/browse/KR1-508

device/고객/계약/설치/보증·양도/교체/폐기 이력을 연결

입력/출력: device id·customer ref·contract·lifecycle epoch

경계시험: 양도·폐기·기기 교체·권한 잔존

지표: mapping 정합성·이력추적·revoke 반영

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-12/F2159/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

등록/고객mapping → 최소 telemetry/관제 → 서명 검증 OTA/canary/rollback → 비용품질/예지정비/A/S. Epic-06 진단·Epic-13 신뢰/비밀·Epic-14 사용량·Epic-16 HW·Epic-20 고객 연결.

필요 입력/연동: 클라우드/DB/배포환경·device cert/ownership·signing/KMS·실제 A/B bootloader·SLO·retention·service 운영자·A/S 부품자료

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
