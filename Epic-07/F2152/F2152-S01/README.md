# [F2152-S01] Network·SLAM Mapping·방 이름 설정 Wizard 요구사항·Interface·Simulation 설계

Jira: https://lumira077.atlassian.net/browse/KR1-314

Interface/TF·clock·state·제어주기·QoS·Simulation 설계: 연결→지도 작성→방 이름/금지구역→저장·재개 Wizard를 구성

데이터: network ref·map revision·room id·zone·step

검증: 불완전지도·가구변경·네트워크 끊김·중복 방 이름

지표: 온보딩 완료율·재개 일관성·설정 보존

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
