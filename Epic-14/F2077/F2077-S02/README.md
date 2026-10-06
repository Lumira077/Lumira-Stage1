# [F2077-S02] 구독 플랜 및 권한 관리 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-622

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: 공통 entitlement 조회를 plan/사용자/모델/epoch에 맞춰 구성

데이터: plan version·feature scopes·device·effective time

검증: 구독만료·철회·offline grace·cache stale

지표: 권한정확성·revoke 지연·우회 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
