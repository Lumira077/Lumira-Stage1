# [F2146-S02] 양팔 협조 제어·재파지·지원 요청 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-371

ROS2/제어/센서·actuator adapter 구현 및 version 관리: 양팔 trajectory 동기화·하중분배·재파지와 지원 요청을 구성

데이터: paired trajectories·sync·load·grasp state

검증: 한 팔 고장·동기 손실·편하중·slip

지표: 상대 pose 오차·동기 skew·복구율

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
