# [F2054] 연령별 교육 프로필

Jira: https://lumira077.atlassian.net/browse/KR1-406

보호자 승인 연령대·관심·수준으로 교육 프로필과 제한을 구성

입력/출력: age band·level·interest·guardian scope

경계시험: 연령 Unknown·권한 철회·차별적 분류

지표: 연령적합성·최소수집·권한 일치

구현 범위: partial_offline_utility; 공통 utility: kids_catalog. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-10/F2054/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

보호자 승인 프로필 → 검수 퀴즈/동화/언어/놀이 → 진도/공유. Epic-01 개인화·Epic-02 대화·Epic-04 표현·Epic-11 부모 통제·Epic-13 보호·Epic-14 권리/구독 연결.

필요 입력/연동: 연령/수준 rubric·검수/권리 콘텐츠·보호자 동의·평가 참가자·승인 motion/음량/시간 제한

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
