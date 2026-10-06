# [F2216] Subscription Plan Management

Jira: https://lumira077.atlassian.net/browse/KR1-595

plan version·trial·upgrade/downgrade·proration·권한시점을 관리

입력/출력: plan id·effective time·credit·price·entitlement

경계시험: 월중변경·취소·가격버전·과거요금제

지표: 변경일관성·일할계산·권한시점

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-14/F2216/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

router cost/usage → quota/plan/entitlement → Test PG billing/renewal/refund → settlement/anomaly → 예외 automation/추천/catalog. F2216 요금제와 F2077 권한, F2217 PG adapter와 F2080 billing lifecycle, F2215 quota와 F2079 usage의 책임/원장을 분리한다.

필요 입력/연동: 요금제/가격/credit/환불 승인정책·Test PG 계정/Secret·회계대사·콘텐츠 권리·n8n endpoint/인증·provider usage receipt

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
