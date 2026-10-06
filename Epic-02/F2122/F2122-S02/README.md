# F2122-S02

Jira: https://lumira077.atlassian.net/browse/KR1-130

- 모델 manifest·메모리/온도 gate·허용 Tool proposal 검증기를 구현
- LocalModelGate 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 선정 모델을 실제 보드에서 실행해 RAM/first token/속도/발열 목표와 승인 Tool 검증을 통과한다.

현재 제한: 현재 자원/Tool gate만 구현; 모델 다운로드·실제 추론·RK3588 NPU/Jetson 가속·실물 benchmark 미실시

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
