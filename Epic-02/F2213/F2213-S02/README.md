# F2213-S02

Jira: https://lumira077.atlassian.net/browse/KR1-85

- 정해진 Provider/status 숫자 메타데이터만 허용하는 수집기·p50/p95·성공률 집계 구현
- QualityTelemetry 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: Provider·모델·요금제별 대시보드가 운영 데이터로 검증되며 민감 로그와 추정 비용을 분리한다.

현재 제한: 현재 메모리 집계와 JSON report; 실제 metrics backend·대시보드·보존/삭제·청구 데이터 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
