# [F2046-S01] 간단 심부름 임무 실행 요구사항·Interface·Simulation 설계

Jira: https://lumira077.atlassian.net/browse/KR1-340

Interface/TF·clock·state·제어주기·QoS·Simulation 설계: 심부름 요청을 탐색/이동/파지/운반/전달 단계와 취소·지원 요청으로 분해

데이터: task id·steps·object·recipient·precondition

검증: 대상 없음·사용자 변경·중단·partial failure

지표: 임무 성공률·복구율·중복 실행 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
