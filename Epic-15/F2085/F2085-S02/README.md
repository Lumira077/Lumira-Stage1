# [F2085-S02] 스마트홈 기기 연동 알고리즘·제어기·HW 연동 구현

Jira: https://lumira077.atlassian.net/browse/KR1-673

ROS2/제어/센서·actuator adapter 구현 및 version 관리: 승인 기기 목록의 상태조회·제어·결과확인을 Stage2부터 구성

데이터: device id·capability·command·state revision

검증: 미승인기기·offline·state mismatch·민감기기

지표: 호환성·실행확인·권한차단

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
