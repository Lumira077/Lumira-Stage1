# KR1-6 / F2001 완료조건 추적

| 하위 항목 | 소스·산출물·검증 | 완료 범위 / 남은 증적 |
|---|---|---|
| T01 사용자 검증 계획 | user-study.md / evaluate_users | 계획·형식 구현, 실제 연구 승인·모집 필요 |
| T02 실제 사용자 시나리오 | study-simulated.json / study-evaluation.json | 6과업 예시, 실제 참여 0명 |
| T03 개선·재시험 | baseline/retest·후보 version·중복 방지 | 실제 문제·수정·재시험 기록 필요 |
| T04 운영지표 | metrics.py / metrics*.json / tests/test_ops.py | 코호트·경로·버전·시도별 집계, 실제 운영 기준 필요 |
| T05 로그·Dashboard | telemetry.py / service.py / dashboard.py | 가명·필드 제한·정적 화면, 운영 API·모니터링 연결 필요 |
| T06 대응 절차 | runbook.md / alerts | 제안 경보·절차, 책임자/SLO/경보 승인 필요 |
| T07 사용자 안내 | user-guide.md | 개발 안내 작성, 실사용 검토 필요 |
| T08 manifest·notes | manifest.json / release-notes.md | 버전·고정 의존성·미확정 자산 명시 |
| T09 배포·rollback | restore.py / deployment.md / tests/test_service_restore.py | sandbox 백업·삭제/철회 재적용, 실제 배포·복귀 필요 |
| T10 F2001 연결·Release | dependency.json / release.py / release-gate.json | S02/S03 고정 연결 및 증적 digest, Q1/R1 승인 필요 |

F2001의 등록·준비·재개·취소 및 개인정보 보호 완료조건에 연결한다. S01은 설계, S02는 핵심 서비스, S03은 로봇 통합 시험, S04는 검증·운영·Release 판정이다. 소프트웨어 시험 통과를 F2001 전체 또는 KR1-6 Done으로 해석하지 않는다. 실제 연구/실기/운영/복귀/결함 및 검토 승인 증적 위치는 Jira에 추가해야 한다.
