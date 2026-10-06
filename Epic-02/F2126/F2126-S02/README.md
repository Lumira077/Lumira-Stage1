# F2126-S02

Jira: https://lumira077.atlassian.net/browse/KR1-140

- 유한 PCM 검증·채널 평균 beam 샘플·고정계수 reference subtraction·지연→DOA 기하 계산 구현
- AudioLab 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 실제 TTS 재생·잡음·거리/방향 조건에서 AEC/DOA/STT 품질 목표를 충족하며 DOA를 사용자 인증으로 사용하지 않는다.

현재 제한: 현재 기초 DSP 계산·계약 시험. adaptive AEC·실제 beamformer·TDOA 추정·마이크 배열·실물 성능 미구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
