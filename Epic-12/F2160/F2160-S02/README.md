# [F2160-S02] Robot Fleet 운영 Dashboard 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-515

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: 고객/모델/지역/버전별 fleet 상태·경보·지원 drilldown을 설계

데이터: fleet filter·device state·permissions·KPI

검증: cross-tenant·대량 fleet·stale·필터 오류

지표: 권한별 집계·freshness·탐색시간

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
