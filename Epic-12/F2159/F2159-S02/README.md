# [F2159-S02] Device-Customer Mapping·Lifecycle 관리 서비스·App·자동화 구현

Jira: https://lumira077.atlassian.net/browse/KR1-510

핵심 서비스/adapter 계획·재현 환경·구현 범위와 미연동 표시: device/고객/계약/설치/보증·양도/교체/폐기 이력을 연결

데이터: device id·customer ref·contract·lifecycle epoch

검증: 양도·폐기·기기 교체·권한 잔존

지표: mapping 정합성·이력추적·revoke 반영

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
