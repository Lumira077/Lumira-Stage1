# [F2143-S02] 물체 재질·취약성 추정 및 Unknown 안전정책 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-356

ROS2/제어/센서·actuator adapter 구현 및 version 관리: vision/접촉으로 재질·취약성을 추정하고 Unknown일 때 보수적인 파지 정책을 적용

데이터: material·fragility·confidence·approved force

검증: 유리/도자기/연질·충돌 정보·낮은 신뢰

지표: 재질 분류·Unknown 거절·파손 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
