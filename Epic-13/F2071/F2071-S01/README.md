# [F2071-S01] 사용자 동의 및 개인정보 설정 위험분석·보안요구·검증계획

Jira: https://lumira077.atlassian.net/browse/KR1-530

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: 목적별 consent version·철회·보유·삭제 전파를 구성

데이터: subject·purpose·consent version·epoch·retention

검증: 철회 후 queued job·다른 사용자·백업 복원

지표: 철회 반영시간·삭제 검증·목적외 수집 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
