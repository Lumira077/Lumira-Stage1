# F2014-S01

Jira: https://lumira077.atlassian.net/browse/KR1-119

- 연령 미확정·아동·의료·위기·폭력·개인정보 정책과 한계 안내·정정·상담 연결 범위 정의
- SafetyContext: age_band, risk_class, policy_version; Review: action, reason, safe_template의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- SafetyPolicy.review(classified_request,response); 실제 semantic 분류/출력 검증을 운영 모델에 연결의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 승인된 연령/위기 평가집합에서 위험 응답 기준을 충족하고 의료·긴급 대응 수행을 허위 주장하지 않는다.

현재 제한: 현재 태그 기반 정책 gate; 실제 의미 분류·유해성 검출·전문가 검토·긴급 연락 서비스 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
