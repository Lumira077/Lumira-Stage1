# EPIC-12 클라우드·관제·OTA 운영

https://lumira077.atlassian.net/browse/KR1-472

11 Features, 44 existing Sub-tasks.

등록/고객mapping → 최소 telemetry/관제 → 서명 검증 OTA/canary/rollback → 비용품질/예지정비/A/S. Epic-06 진단·Epic-13 신뢰/비밀·Epic-14 사용량·Epic-16 HW·Epic-20 고객 연결.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2065] 로봇 등록 및 디지털 자산 관리](F2065/README.md): device identity·serial·모델/HW/SW·고객 등록과 lifecycle을 구성
- [[F2066] 원격 상태 모니터링](F2066/README.md): heartbeat/배터리/온도/장애의 freshness·경보·offline를 구성
- [[F2067] 로그·이벤트·진단 수집](F2067/README.md): 최소 telemetry allowlist·buffer·재전송·retention·삭제를 구성
- [[F2068] OTA 소프트웨어 업데이트](F2068/README.md): 서명·hash·호환성·version·전원/안전 preflight와 A/B 설치를 설계
- [[F2069] 단계적 배포 및 롤백](F2069/README.md): canary/cohort·건강 gate·중단·이전 검증 이미지 롤백을 구성
- [[F2070] 원격 지원 및 설정 관리](F2070/README.md): 동의한 원격진단 세션·허용 설정 patch·TTL·감사·회수 기능을 구성
- [[F2124] AI 비용·지연·품질 운영 모니터링](F2124/README.md): AI route별 비용/지연/오류/품질·예산 경보를 집계
- [[F2159] Device-Customer Mapping·Lifecycle 관리](F2159/README.md): device/고객/계약/설치/보증·양도/교체/폐기 이력을 연결
- [[F2160] Robot Fleet 운영 Dashboard](F2160/README.md): 고객/모델/지역/버전별 fleet 상태·경보·지원 drilldown을 설계
- [[F2161] 원격 진단·Predictive Maintenance](F2161/README.md): 전원/배터리/모터/온도 이력과 근거로 정비 후보를 제안
- [[F2162] A/S Ticket·부품·정비 이력 관리](F2162/README.md): A/S ticket·device/부품/방문/수리/교체·고객 승인 이력을 관리
