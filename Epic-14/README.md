# EPIC-14 콘텐츠·구독·서비스 운영

https://lumira077.atlassian.net/browse/KR1-584

14 Features, 56 existing Sub-tasks.

router cost/usage → quota/plan/entitlement → Test PG billing/renewal/refund → settlement/anomaly → 예외 automation/추천/catalog. F2216 요금제와 F2077 권한, F2217 PG adapter와 F2080 billing lifecycle, F2215 quota와 F2079 usage의 책임/원장을 분리한다.

현재 명세/검토 도구·일부 로컬 utility입니다. 실제 HW·production서비스·Pilot·법률/재무 승인·외부 실행은 미완료입니다.

- [[F2214] AI Router 및 Model Cost Optimization](F2214/README.md): route/model 가격버전·품질 gate·Local 확대의 비용 정책을 설계
- [[F2215] AI Credit 및 Quota Management](F2215/README.md): credit weight·월한도·예약/확정/취소·grace/차단을 구성
- [[F2216] Subscription Plan Management](F2216/README.md): plan version·trial·upgrade/downgrade·proration·권한시점을 관리
- [[F2217] Payment Gateway Integration](F2217/README.md): Test PG 승인/실패/취소/환불·webhook 서명·idempotency를 연결
- [[F2218] Monthly Settlement 및 Revenue Analytics](F2218/README.md): 월 매출·환불·PG 수수료·AI원가를 통화별 대사
- [[F2219] Billing Anomaly Detection](F2219/README.md): 중복청구·비정상 credit·결제실패율·정산차이 룰을 구성
- [[F2220] Jira 및 n8n Billing Exception Automation](F2220/README.md): billing exception event를 dedup key로 Jira/n8n proposal에 연결
- [[F2077] 구독 플랜 및 권한 관리](F2077/README.md): 공통 entitlement 조회를 plan/사용자/모델/epoch에 맞춰 구성
- [[F2078] 콘텐츠 카탈로그 및 배포](F2078/README.md): 콘텐츠 license·age band·검수·version·cache/rollback을 구성
- [[F2079] AI 사용량 계측 및 비용 제어](F2079/README.md): 토큰/음성/영상/Cloud 사용량을 idempotent 원가계측으로 구성
- [[F2080] 결제·청구·구독 갱신 및 PG 연동](F2080/README.md): PG·구독 갱신·청구·receipt·취소/환불 lifecycle을 구성
- [[F2081] 콘텐츠 추천 및 구독 서비스 분석](F2081/README.md): 동의/age/권한·비용·사용량에 기반한 추천과 분석을 구성
- [[F2158] Fashion·Accessory 상품·Catalog 운영](F2158/README.md): Fashion/Accessory SKU·모델 호환·재고·NFC·테마권리를 관리
- [[F2163] 사용량 기반 구독·추가 Service Recommendation](F2163/README.md): 동의 usage 기반 추가 서비스 추천과 해지/수락 이력을 구성
