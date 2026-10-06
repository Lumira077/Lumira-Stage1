# F2211-S02

Jira: https://lumira077.atlassian.net/browse/KR1-75

- sensitive/unknown·미동의·안전 요청 fail-closed 및 Cloud 최소 payload 구조 구현
- PrivacyGuard 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 승인된 시험 집합에서 금지 전송 0건이며 policy/consent version이 감사 메타데이터에 남는다.

현재 제한: 분류 등급은 신뢰된 호출자 입력. 실제 PII 탐지·동의 이벤트·완전한 익명화·전송 감사 미구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
