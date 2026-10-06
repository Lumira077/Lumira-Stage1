# [F2163-S02] 사용량 기반 구독·추가 Service Recommendation 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-652

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: 동의 usage 기반 추가 서비스 추천과 해지/수락 이력을 구성

데이터: aggregate usage·plan·consent·reason·outcome

검증: 민감추론·무동의·과도한 upsell·거절

지표: 근거 추적·수락/거절·부적합 제안

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
