# [F2142-S03] 손끝 Force·Tactile Sensor HW 통합 통합·경계조건·안전 시험

Jira: https://lumira077.atlassian.net/browse/KR1-352

실물/통신/한계·고장주입·물리 ACK·안전 시험: 손끝 force/tactile HW의 배선·sample·calibration·교체 가능 구조를 설계

데이터: sensor id·N/kPa·raw ref·zero·scale·stamp

검증: 포화·단선·drift·교체 후 오보정

지표: 보정오차·대역폭·내구·stale 탐지

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
