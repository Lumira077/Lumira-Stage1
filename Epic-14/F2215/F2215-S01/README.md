# [F2215-S01] AI Credit 및 Quota Management 사용 흐름·Data Model·API 설계

Jira: https://lumira077.atlassian.net/browse/KR1-591

요구사항·데이터/API·오류/동의·시험 기준 및 검토 초안: credit weight·월한도·예약/확정/취소·grace/차단을 구성

데이터: usage id·credit units·reservation·quota epoch

검증: 동시요청·중복·retry·월경계

지표: credit 정합성·초과 차단·중복차감 0건

현재는 task.json 작업계약/증적 요구입니다. 실제 단계 수행 완료는 아닙니다. 상위 contract.json 및 Development/runtime/review.py를 함께 사용합니다. 실제 대상에 맞춘 adapter·검토·시험·승인은 후속입니다.
