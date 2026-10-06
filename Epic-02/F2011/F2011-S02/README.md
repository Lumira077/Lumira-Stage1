# F2011-S02

Jira: https://lumira077.atlassian.net/browse/KR1-105

- 사용자별 메모리 세션·bounded history·switch/expire/cancel 무효화 구현
- ConversationSession 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 사용자 간 문맥 노출 0건, 정해진 상한 유지, 삭제·취소된 세션의 늦은 응답 폐기.

현재 제한: 현재 단일 프로세스 일시 메모리; 인증·분산 세션·durable 요약·자동 동의 이벤트 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
