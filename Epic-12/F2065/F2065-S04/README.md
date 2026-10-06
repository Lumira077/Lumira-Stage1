# [F2065-S04] 로봇 등록 및 디지털 자산 관리 운영 Dashboard·SLA·Release

Jira: https://lumira077.atlassian.net/browse/KR1-477

운영 지표·검토/배포·중단/rollback·완료증적 기준: device identity·serial·모델/HW/SW·고객 등록과 lifecycle을 구성

데이터: device id·serial·model·version·tenant

검증: 중복 serial·위조 등록·교체·폐기

지표: 중복 자산 0건·등록 감사·소유자 일치

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
