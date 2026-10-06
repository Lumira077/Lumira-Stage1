# F2008-S02

Jira: https://lumira077.atlassian.net/browse/KR1-90

- 검출 이벤트 gate·확인 임계치·debounce/cooldown·session epoch 연결 구현
- WakeGate 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 실기 호출·비호출 데이터에서 승인된 FAR/FRR와 지연을 충족하고 mute/에코로 세션이 시작되지 않는다.

현재 제한: 현재 detector score 입력 gate만 구현; 실제 wakeword 모델·발음 학습·마이크·AEC 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
