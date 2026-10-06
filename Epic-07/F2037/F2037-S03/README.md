# [F2037-S03] 실내 지도 작성(SLAM) 통합·경계조건·안전 시험

Jira: https://lumira077.atlassian.net/browse/KR1-291

실물/통신/한계·고장주입·물리 ACK·안전 시험: SLAM pose graph·loop closure·OccupancyGrid 저장/복구와 지도 revision을 관리

데이터: map/posegraph·resolution·origin·frame·revision

검증: 동적 물체·반복 무늬·지도 손상·재시작

지표: ATE/RPE·지도 오차·loop closure 실패

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
