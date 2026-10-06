# [F2066-S01] 원격 상태 모니터링 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-479

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: heartbeat/배터리/온도/장애의 freshness·경보·offline를 구성

데이터: device metadata·heartbeat·metrics·TTL

검증: 중복/지연·network partition·온도 Unknown

지표: 수집지연·availability·stale 오표시

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
