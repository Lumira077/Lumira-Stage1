# [F2084-S01] 가사 작업 계획 요구사항·Interface·Simulation 설계

Jira: https://lumira077.atlassian.net/browse/KR1-667

Interface/TF·clock·state·제어주기·QoS·Simulation 설계: 가사 요청을 자원/안전 precondition·navigation/manipulation 단계로 분해

데이터: task DAG·resources·preconditions·cancel epoch

검증: 불가능 작업·partial failure·열/날카로운 물체

지표: 완료율·재계획·미승인 작업 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
