# [F2218-S02] Monthly Settlement 및 Revenue Analytics 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-607

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: 월 매출·환불·PG 수수료·AI원가를 통화별 대사

데이터: ledger·settlement period·tax ref·fees·provider usage

검증: 기간경계·정산차이·통화 혼합·반올림

지표: 대사차이·마감시간·근거 연결

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
