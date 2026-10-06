# [F2220-S01] Jira 및 n8n Billing Exception Automation 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-616

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: billing exception event를 dedup key로 Jira/n8n proposal에 연결

데이터: exception id·correlation·severity·ticket ref

검증: 중복 event·webhook retry·sync loop·Secret 노출

지표: 동일 event 1건·sync 지연·회복률

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
