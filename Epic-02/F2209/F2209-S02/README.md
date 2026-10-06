# F2209-S02

Jira: https://lumira077.atlassian.net/browse/KR1-65

- 정수 credit ledger의 예약·잔액·멱등 키·정산·실패 환불 Prototype 구현
- Budget 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 동시 요청에도 한도를 넘지 않고 미확인 사용량을 0원으로 확정하지 않으며 가격 버전을 기록한다.

현재 제한: 단일 프로세스 메모리 ledger. 실제 F2079/F2080·분산 원장·Provider usage·가격/환율·청구 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
