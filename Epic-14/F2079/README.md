# [F2079] AI 사용량 계측 및 비용 제어

Jira: https://lumira077.atlassian.net/browse/KR1-630

토큰/음성/영상/Cloud 사용량을 idempotent 원가계측으로 구성

입력/출력: usage id·units·price version·credit·budget

경계시험: 중복계측·추정/확정 차이·할당초과

지표: 원가오차·집계지연·한도차단

구현 범위: partial_offline_utility; 공통 utility: UsageLedger. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-14/F2079/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

router cost/usage → quota/plan/entitlement → Test PG billing/renewal/refund → settlement/anomaly → 예외 automation/추천/catalog. F2216 요금제와 F2077 권한, F2217 PG adapter와 F2080 billing lifecycle, F2215 quota와 F2079 usage의 책임/원장을 분리한다.

필요 입력/연동: 요금제/가격/credit/환불 승인정책·Test PG 계정/Secret·회계대사·콘텐츠 권리·n8n endpoint/인증·provider usage receipt

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.

## 2026-10-06 영속 원장 시제품

`Development/runtime/ledger_sqlite.py`의 SQLiteUsageLedger 추가. 재시작 후 차감/환불 중복 방지, 정수 quota, BEGIN IMMEDIATE 동시 writer 직렬화. DB별 단일 계정, 생성 시 quota 고정. 8개 시험 통과. 월별 갱신·예약/확정·인증·암호화·외부 결제·provider receipt·운영 DB 마이그레이션은 미구현.
