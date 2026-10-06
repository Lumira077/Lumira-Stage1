# F2208-S02

Jira: https://lumira077.atlassian.net/browse/KR1-60

- 사용자 격리·확인 상태·TTL·top-k·Cloud 별도 공유 허용 필터와 lexical 검색 구현
- LocalContext 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 권한별 조회가 분리되고 미승인 기억이 Cloud로 전달되지 않으며 로컬 평가셋 검색 목표를 충족한다.

현재 제한: 현재 합성 fixture lexical 검색. 실제 F2003 ticket·동의 epoch·벡터/임베딩·운영 암호화/삭제 연동은 추가 구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
