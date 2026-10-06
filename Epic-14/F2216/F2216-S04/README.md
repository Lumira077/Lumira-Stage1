# [F2216-S04] Subscription Plan Management 운영 Dashboard·SLA·Release

Jira: https://lumira077.atlassian.net/browse/KR1-599

운영 지표·검토/배포·중단/rollback·완료증적 기준: plan version·trial·upgrade/downgrade·proration·권한시점을 관리

데이터: plan id·effective time·credit·price·entitlement

검증: 월중변경·취소·가격버전·과거요금제

지표: 변경일관성·일할계산·권한시점

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
