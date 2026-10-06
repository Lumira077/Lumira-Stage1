# [F2163] 사용량 기반 구독·추가 Service Recommendation

Jira: https://lumira077.atlassian.net/browse/KR1-650

동의 usage 기반 추가 서비스 추천과 해지/수락 이력을 구성

입력/출력: aggregate usage·plan·consent·reason·outcome

경계시험: 민감추론·무동의·과도한 upsell·거절

지표: 근거 추적·수락/거절·부적합 제안

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-14/F2163/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

router cost/usage → quota/plan/entitlement → Test PG billing/renewal/refund → settlement/anomaly → 예외 automation/추천/catalog. F2216 요금제와 F2077 권한, F2217 PG adapter와 F2080 billing lifecycle, F2215 quota와 F2079 usage의 책임/원장을 분리한다.

필요 입력/연동: 요금제/가격/credit/환불 승인정책·Test PG 계정/Secret·회계대사·콘텐츠 권리·n8n endpoint/인증·provider usage receipt

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
