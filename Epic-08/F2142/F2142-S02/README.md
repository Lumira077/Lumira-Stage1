# [F2142-S02] 손끝 Force·Tactile Sensor HW 통합 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-351

ROS2/제어/센서·actuator adapter 구현 및 version 관리: 손끝 force/tactile HW의 배선·sample·calibration·교체 가능 구조를 설계

데이터: sensor id·N/kPa·raw ref·zero·scale·stamp

검증: 포화·단선·drift·교체 후 오보정

지표: 보정오차·대역폭·내구·stale 탐지

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
