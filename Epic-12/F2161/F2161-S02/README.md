# [F2161-S02] 원격 진단·Predictive Maintenance 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-520

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: 전원/배터리/모터/온도 이력과 근거로 정비 후보를 제안

데이터: device series·fault·maintenance threshold·evidence

검증: 센서 누락·오탐·cold start·모델 drift

지표: 예측 precision/recall·정비lead time·coverage

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
