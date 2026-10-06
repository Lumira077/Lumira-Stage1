# [F2148-S01] 자연어 IoT 제어·실행 확인 요구사항·Interface·Simulation 설계

Jira: https://lumira077.atlassian.net/browse/KR1-702

Interface/TF·clock·state·제어주기·QoS·Simulation 설계: 자연어를 allowlisted IoT intent로 변환하고 민감명령 확인·receipt를 구성

데이터: intent·device/room·action·confirmation·receipt

검증: ambiguous target·prompt injection·late ACK

지표: intent 정확성·실행확인·미승인 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
