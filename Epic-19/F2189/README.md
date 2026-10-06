# [F2189] 투자금 집행·KPI 보고·후속투자 준비

Jira: https://lumira077.atlassian.net/browse/KR1-1036

승인 use-of-funds와 집행/개발/매출 KPI·runway·후속round를 관리

입력/출력: budget version·expenses·cash·milestone·report

경계시험: 예산초과·수치누락·조달지연·성과미달

지표: 계획vs실적·runway·보고근거

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-19/F2189/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

목표round/use-of-funds → Data Room/재무/IR·Demo/PoC → 정부matching/검증 investor CRM → 승인접촉/실사/협상/계약 → 실제입금/집행. 첨부 과거 사업 가정은 최신 승인 재무계획과 구분하며 수요/LOI를 매출/투자확정으로 표시하지 않는다.

필요 입력/연동: 최신 KER 자금/재무/주주/계약·판매/원가 가정·투자목표·검증된 Demo·동의 연락처/실제미팅·회계/법률 검토·공고 원문

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
