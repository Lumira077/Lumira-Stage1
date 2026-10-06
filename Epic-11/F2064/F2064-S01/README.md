# [F2064-S01] 보호자 음성·영상 통화 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-458

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: 사용자 수락·camera/mic 표시·암호화 통화·즉시 종료를 설계

데이터: call id·participants·consent·signaling·ICE

검증: 수락 없음·네트워크 전환·권한 철회·도청

지표: 연결성·종료반영·원문 비저장

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
