# F2207-S02

Jira: https://lumira077.atlassian.net/browse/KR1-55

- 메타데이터 세션 gate와 최신 epoch·sequence·전송 한도·영상 필요 조건 구현
- RealtimeGate 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 실제 음성·영상의 시각 동기화와 종료·재연결을 확인하고 필요 없는 영상 전송을 차단한다.

현재 제한: 실제 WebRTC/WebSocket·카메라·마이크·영상/음성 동의 UI·시각 모델 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
