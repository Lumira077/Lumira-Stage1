# [F2067-S01] 로그·이벤트·진단 수집 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-484

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: 최소 telemetry allowlist·buffer·재전송·retention·삭제를 구성

데이터: event id·schema·code·stamp·retention

검증: 원문/Secret 포함·overflow·중복·offline

지표: 유실률·중복률·민감원문 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
