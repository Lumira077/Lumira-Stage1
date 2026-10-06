# [F2068] OTA 소프트웨어 업데이트

Jira: https://lumira077.atlassian.net/browse/KR1-488

서명·hash·호환성·version·전원/안전 preflight와 A/B 설치를 설계

입력/출력: manifest·signature ref·digest·HW revision·slot

경계시험: 서명위조·다운그레이드·전원단절·용량부족

지표: 검증 실패 차단·부팅 성공·복구시간

구현 범위: partial_offline_utility; 공통 utility: ota_preflight. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-12/F2068/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

등록/고객mapping → 최소 telemetry/관제 → 서명 검증 OTA/canary/rollback → 비용품질/예지정비/A/S. Epic-06 진단·Epic-13 신뢰/비밀·Epic-14 사용량·Epic-16 HW·Epic-20 고객 연결.

필요 입력/연동: 클라우드/DB/배포환경·device cert/ownership·signing/KMS·실제 A/B bootloader·SLO·retention·service 운영자·A/S 부품자료

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
