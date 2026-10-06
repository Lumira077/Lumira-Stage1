# F2212-S02

Jira: https://lumira077.atlassian.net/browse/KR1-80

- 허용 횟수 failover·최종 응답 한 번 확정·부분 출력 후 자동 재발화 차단
- Recovery 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 원인과 attempt를 기록하고 목표 복구시간 내 전환하며 동일 turn의 최종 출력이 중복되지 않는다.

현재 제한: 실제 Provider retry/circuit breaker·stream cancellation·timeout 제어·부분 오디오 복귀 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
