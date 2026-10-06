# [F2153-S03] 사용자·IoT·권한 부분 재설정 통합·보안·부하·복구 시험

Jira: https://lumira077.atlassian.net/browse/KR1-470

정상/예외/경계조건·실제 통합 검증 계획·근거/재시험: 사용자·IoT·권한의 선택 변경과 참조 무결성·소유권 epoch 갱신을 구성

데이터: reset scope·revision·dependent ids·epoch

검증: 이사·가구변경·사용자 추가·기기 교체

지표: 비대상 데이터 보존·참조 일치·권한 revoke

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
