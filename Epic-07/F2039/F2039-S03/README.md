# [F2039-S03] 목적지 경로 계획 및 추종 통합·경계조건·안전 시험

Jira: https://lumira077.atlassian.net/browse/KR1-301

실물/통신/한계·고장주입·물리 ACK·안전 시험: 목적지/금지구역을 검증하고 global/local 경로 및 취소·재계획을 연결

데이터: goal·footprint·costmap·path·cmd_vel·generation

검증: 도달 불가·지도 변경·late command·timeout

지표: 도달률·경로 길이·추종오차·정지 ACK

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
