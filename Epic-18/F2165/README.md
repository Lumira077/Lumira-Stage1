# [F2165] 특허 Governance·발명관리 Process

Jira: https://lumira077.atlassian.net/browse/KR1-934

발명신고·발명자/권리자·공개전검토·분류/예산/책임 프로세스를 구성

입력/출력: invention id·inventors·owner·disclosure·evidence

경계시험: 공개 선행·권리귀속 불명·기한누락

지표: 승인추적·공개전검토coverage·책임자

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-18/F2165/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

발명신고/공개gate → 검색/family/claim map → 국내/해외/심사/유지 → 국가·출시버전별 FTO/라이선스. Epic-01~17 기술 증적과 Epic-19 실사·Epic-20 공개일정 연결. 검색결과·법적상태·기한·특허가능성/FTO 결론은 실제 조사와 변리사 검토가 필요하다.

필요 입력/연동: 발명자/권리자·비공개 기술자료·선행문헌/claim·국가/제품 version·변리사 검토·공식 기한/접수증·IP 예산

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
