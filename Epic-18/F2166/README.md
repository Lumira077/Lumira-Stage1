# [F2166] 기술·경쟁사 Patent Landscape 및 선행기술 조사

Jira: https://lumira077.atlassian.net/browse/KR1-939

분야별 특허/논문검색식을 저장하고 family/법적상태·claim element를 분류

입력/출력: query·jurisdiction·publication·family·claim·source date

경계시험: 번역오류·중복family·상태 stale·검색공백

지표: 검색재현성·claim 근거·전문가 검토

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-18/F2166/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

발명신고/공개gate → 검색/family/claim map → 국내/해외/심사/유지 → 국가·출시버전별 FTO/라이선스. Epic-01~17 기술 증적과 Epic-19 실사·Epic-20 공개일정 연결. 검색결과·법적상태·기한·특허가능성/FTO 결론은 실제 조사와 변리사 검토가 필요하다.

필요 입력/연동: 발명자/권리자·비공개 기술자료·선행문헌/claim·국가/제품 version·변리사 검토·공식 기한/접수증·IP 예산

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
