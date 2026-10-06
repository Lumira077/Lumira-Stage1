# [F2175] 등록·연차료·권리평가·영업비밀 관리

Jira: https://lumira077.atlassian.net/browse/KR1-984

등록/연차료/존속·유지포기/영업비밀·권리평가를 기록

입력/출력: registration·annuity verified due·owner·decision

경계시험: 미납·양도·공개·영업비밀 접근

지표: 최신권리상태·기한근거·결정추적

구현 범위: partial_offline_utility; 공통 utility: docket_review. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-18/F2175/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

발명신고/공개gate → 검색/family/claim map → 국내/해외/심사/유지 → 국가·출시버전별 FTO/라이선스. Epic-01~17 기술 증적과 Epic-19 실사·Epic-20 공개일정 연결. 검색결과·법적상태·기한·특허가능성/FTO 결론은 실제 조사와 변리사 검토가 필요하다.

필요 입력/연동: 발명자/권리자·비공개 기술자료·선행문헌/claim·국가/제품 version·변리사 검토·공식 기한/접수증·IP 예산

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
