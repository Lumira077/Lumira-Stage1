# [F2137-S02] Stage4 가변 높이 범위·승강 Mechanism 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-688

ROS2/제어/센서·actuator adapter 구현 및 version 관리: 700~1200mm 구상 목표의 승강·limit·position·구조를 설계 검증

데이터: stroke·height·load·drawing·limit·calibration

검증: 끼임·중간전원단절·기울기·과부하

지표: 강성·위치오차·승강수명·정지

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
