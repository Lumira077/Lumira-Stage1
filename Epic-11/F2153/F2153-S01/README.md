# [F2153-S01] 사용자·IoT·권한 부분 재설정 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-468

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: 사용자·IoT·권한의 선택 변경과 참조 무결성·소유권 epoch 갱신을 구성

데이터: reset scope·revision·dependent ids·epoch

검증: 이사·가구변경·사용자 추가·기기 교체

지표: 비대상 데이터 보존·참조 일치·권한 revoke

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
