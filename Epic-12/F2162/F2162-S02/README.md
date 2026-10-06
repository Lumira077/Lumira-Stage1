# [F2162-S02] A/S Ticket·부품·정비 이력 관리 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-525

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: A/S ticket·device/부품/방문/수리/교체·고객 승인 이력을 관리

데이터: ticket id·device·part serial·status·SLA

검증: 중복 ticket·오부품·재고 부족·미승인 교체

지표: 처리시간·재발률·부품 추적·상태일치

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
