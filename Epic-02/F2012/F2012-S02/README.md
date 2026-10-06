# F2012-S02

Jira: https://lumira077.atlassian.net/browse/KR1-110

- epoch 증가·생성/TTS/motion cancel 요청·late output 거절·ACK 대기상태 구현
- InterruptController 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 실기 TTS/동작 취소 지연 목표와 미취소 출력 0건을 충족하고 ACK 누락 시 재개하지 않는다.

현재 제한: 현재 메타데이터 취소 요청/ACK; 실제 마이크 VAD·TTS/모터 큐·안전 정지 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
