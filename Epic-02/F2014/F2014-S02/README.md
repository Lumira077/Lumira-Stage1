# F2014-S02

Jira: https://lumira077.atlassian.net/browse/KR1-120

- 신뢰된 위험 분류 태그 기반 allow/deny/local guidance·출력 길이 gate 구현
- SafetyPolicy 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 승인된 연령/위기 평가집합에서 위험 응답 기준을 충족하고 의료·긴급 대응 수행을 허위 주장하지 않는다.

현재 제한: 현재 태그 기반 정책 gate; 실제 의미 분류·유해성 검출·전문가 검토·긴급 연락 서비스 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
