# [F2203] Customer Community·VOC·Referral·Retention

Jira: https://lumira077.atlassian.net/browse/KR1-1094

VOC분류/처리·커뮤니티·추천/재구매·retention을 설계

입력/출력: ticket·consent·product revision·referral·cohort

경계시험: 개인정보·중복VOC·무응답·부정추천

지표: 처리SLA·재발·유지/재구매·피드백

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-20/F2203/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

Stage1 Community/Beta/D2C → Stage2 Home/Office·공간/Upgrade → Stage3 Helper 기관PoC/B2B → Stage4 접근성/Care. 공통 consentCRM·VOC/retention·집계funnel 연결. 행사/채널 일정은 공식 근거 확인 후 운영하며 현재 게시/접촉/주문/매출은 실행하지 않았다.

필요 입력/연동: Stage별준비gate·최신 고객/가격/권한·동의CRM·채널계정·실제행사 일정/예산·승인홍보물/계약·주문/설치/회수 증적

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
