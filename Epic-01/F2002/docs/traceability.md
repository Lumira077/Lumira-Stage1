# F2002 완료조건·Jira·소스 연결

| 항목 | 소스·시험·증적 | 남은 실제 완료조건 |
|---|---|---|
| S01 KR1-8 시나리오/입출력/API/오류 | profile_contract, design.md, openapi.json, 15개 계약 시험 | 권한·대표 사용자·실기 제한 설계 승인 |
| S02 KR1-9 핵심 모델/재현 환경 | profile_service, SQLite/API/bridge, 22개 서비스·HTTP 시험 | 운영 인증·암호화·프로필 권위 저장소·동기화 |
| S03 KR1-10 모듈통합/지연/실패복구/안전 | profile_lab, 14개 통합 시험, 저장/적용 각각100회 측정 | 실제 STT/TTS/인식/표정/제어 및 물리 안전 |
| S04 KR1-11 검증/지표/로그/운영/배포 | profile_ops, 16개 지표·복원 시험, Dashboard/Release gate | 실제 연구·운영 기준·배포/복귀·Q1/R1 승인 |

상위 F2002 KR1-7의 설계·구현·모듈 통합에 연결한다. 총 67개 개발 자동 시험. source SHA는 CI report.json으로 고정하고 CI Artifact는 30일 보관한다. 장기 실제 증적은 승인된 저장소에 보관한 뒤 Jira에 링크한다. 실제 사용자/로봇/운영 완료를 개발 성공으로 대체하지 않는다.
