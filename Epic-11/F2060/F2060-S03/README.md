# [F2060-S03] 모바일 앱 계정 및 로봇 연결 통합·보안·부하·복구 시험

Jira: https://lumira077.atlassian.net/browse/KR1-440

정상/예외/경계조건·실제 통합 검증 계획·근거/재시험: 계정 인증·일회 pairing·기기 소유권·가족 초대/해제를 구성

데이터: account·robot id·pair token ref·owner epoch

검증: 토큰 재사용·소유권 변경·분실·권한 상승

지표: pairing 성공률·cross-owner 차단·해제 반영

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
