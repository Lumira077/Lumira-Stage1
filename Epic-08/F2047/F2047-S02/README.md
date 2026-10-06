# [F2047-S02] 사람 근접 조작 안전 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-346

ROS2/제어/센서·actuator adapter 구현 및 version 관리: 사람 근접 조작의 감속·정지·작업영역 제한을 독립 안전경로와 연결

데이터: human distance·trajectory·safety state·ACK

검증: 가림·센서 stale·끼임·AI hang

지표: 최소거리·정지시간·restart interlock

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
