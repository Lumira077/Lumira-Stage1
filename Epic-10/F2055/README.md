# [F2055] 퀴즈·학습 대화

Jira: https://lumira077.atlassian.net/browse/KR1-411

검수 문제은행의 난이도·힌트·정답 feedback·중단을 구성

입력/출력: question id·difficulty·answer·attempt·hint

경계시험: 오답 연속·ASR 불확실·금지내용·시간초과

지표: 정답처리 정확성·학습흐름·피로/중단

구현 범위: spec_and_evidence_tooling_only; 공통 utility: None. Feature 전체의 production 구현을 뜻하지 않습니다.

`python Development/runtime/run.py`로 공통 utility 시험/계약검사를 수행합니다. `python Development/runtime/review.py Epic-10/F2055/contract.json`로 이 Feature의 미연동·누락 단계·완료증적 요구를 확인합니다.

보호자 승인 프로필 → 검수 퀴즈/동화/언어/놀이 → 진도/공유. Epic-01 개인화·Epic-02 대화·Epic-04 표현·Epic-11 부모 통제·Epic-13 보호·Epic-14 권리/구독 연결.

필요 입력/연동: 연령/수준 rubric·검수/권리 콘텐츠·보호자 동의·평가 참가자·승인 motion/음량/시간 제한

실제 HW/사용자/통지/PG/출원/접촉/계약/투자 호출 0. release_ready=false.
