# [F2080-S04] 결제·청구·구독 갱신 및 PG 연동 운영 Dashboard·SLA·Release

Jira: https://lumira077.atlassian.net/browse/KR1-639

운영 지표·검토/배포·중단/rollback·완료증적 기준: PG·구독 갱신·청구·receipt·취소/환불 lifecycle을 구성

데이터: invoice id·subscription·payment·refund·state

검증: 역순/중복 webhook·재시도·갱신중 해지

지표: 금액/상태 정합성·중복 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
