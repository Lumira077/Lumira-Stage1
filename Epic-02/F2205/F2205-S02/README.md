# F2205-S02

Jira: https://lumira077.atlassian.net/browse/KR1-45

- 허용 경로(local/cloud/hybrid/deny)와 reason_code·policy_version을 결정하는 순수 함수 구현
- PolicyEngine 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 동일 입력에 동일 경로/사유를 반환하고 개인정보·안전 금지 조건이 비용/품질 선호에 의해 완화되지 않는다.

현재 제한: 실제 위험 분류기·운영 정책 승인·실시간 로봇/요금제 상태 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
