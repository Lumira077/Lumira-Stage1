# [F2043-S01] 5-Finger 손가락 독립 제어 요구사항·Interface·Simulation 설계

Jira: https://lumira077.atlassian.net/browse/KR1-325

Interface/TF·clock·state·제어주기·QoS·Simulation 설계: 5개 손가락의 독립 joint/synergy 명령과 force·접촉 제한을 구성

데이터: finger joint map·position·force·contact

검증: 과압·걸림·joint 고장·잘못된 finger id

지표: 손가락별 오차·힘 한계·복구시간

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
