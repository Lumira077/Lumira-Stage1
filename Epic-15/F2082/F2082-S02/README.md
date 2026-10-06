# [F2082-S02] 높이 조절 본체 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-658

ROS2/제어/센서·actuator adapter 구현 및 version 관리: Stage4 높이 조절 actuator·absolute position·limit·과부하·끼임 구조를 설계

데이터: height·stroke·encoder·limit switch·load

검증: 상한/하한·과부하·encoder fault·전원단절

지표: 높이 오차·강성·정지거리·전도 안정성

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
