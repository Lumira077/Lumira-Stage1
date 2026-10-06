# [F2061-S03] 로봇 상태 및 알림 조회 통합·보안·부하·복구 시험

Jira: https://lumira077.atlassian.net/browse/KR1-445

정상/예외/경계조건·실제 통합 검증 계획·근거/재시험: 상태 TTL·알림 이력/확인·중복 억제와 offline 표시를 구성

데이터: status stamp·battery·error·alert id·receipt

검증: stale 상태·중복 push·offline·권한 없음

지표: 상태 freshness·알림 지연·중복률

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
