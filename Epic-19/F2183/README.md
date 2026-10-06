# [F2183] 정부 R&D·정책자금·보증·민간투자 Matching

Jira: https://lumira077.atlassian.net/browse/KR1-1016

정부 R&D·보증·정책/민간 matching을공고근거/자격·중복/비용과 연결

입력/출력: program source·eligibility·deadline verified·matching

경계시험: 공고변경·중복수혜·자부담·자격불명

지표: 자격근거·신청검토·실제접수증

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-19/F2183/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

목표round/use-of-funds → Data Room/재무/IR·Demo/PoC → 정부matching/검증 investor CRM → 승인접촉/실사/협상/계약 → 실제입금/집행. 첨부 과거 사업 가정은 최신 승인 재무계획과 구분하며 수요/LOI를 매출/투자확정으로 표시하지 않는다.

필요 입력/연동: 최신 KER 자금/재무/주주/계약·판매/원가 가정·투자목표·검증된 Demo·동의 연락처/실제미팅·회계/법률 검토·공고 원문

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
