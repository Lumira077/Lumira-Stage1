# F2121-S02

Jira: https://lumira077.atlassian.net/browse/KR1-125

- 정규화된 한영 allowlist 명령 parser와 실행 전 action proposal 구현
- LocalCommands 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 실기 기본 명령이 Cloud 호출 없이 목표시간 내 수행되고 긴급 연락/삭제는 실제 실행 증거 없이 완료로 응답하지 않는다.

현재 제한: 현재 정확 문구 parser와 proposal. 실제 제어·삭제·긴급 연락·물리 안전 경로 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
