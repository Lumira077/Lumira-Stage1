# [F2179] 5개년 재무모델·자금사용계획·Unit Economics

Jira: https://lumira077.atlassian.net/browse/KR1-1003

5년수익·원가·구독·A/S·인건비·CAPEX·현금흐름 시나리오를 계산

입력/출력: assumptions·units·price·cost·cash·currency

경계시험: 가격/원가변화·refund·salesdelay·회계기간

지표: cashflow·contribution margin·runway·sensitivity

구현 범위: partial_offline_utility; 공통 utility: cashflow. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-19/F2179/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

목표round/use-of-funds → Data Room/재무/IR·Demo/PoC → 정부matching/검증 investor CRM → 승인접촉/실사/협상/계약 → 실제입금/집행. 첨부 과거 사업 가정은 최신 승인 재무계획과 구분하며 수요/LOI를 매출/투자확정으로 표시하지 않는다.

필요 입력/연동: 최신 KER 자금/재무/주주/계약·판매/원가 가정·투자목표·검증된 Demo·동의 연락처/실제미팅·회계/법률 검토·공고 원문

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
