# [F2044-S01] 조작 대상 물체 인식 및 자세 추정 요구사항·Interface·Simulation 설계

Jira: https://lumira077.atlassian.net/browse/KR1-330

Interface/TF·clock·state·제어주기·QoS·Simulation 설계: RGB-D 기반 물체 종류·6D pose·uncertainty와 파지 후보를 구성

데이터: object id·pose·frame·mask·size·confidence

검증: 투명/반사·가림·frame 불일치·Unknown

지표: pose 오차·인식률·오파지 후보

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
