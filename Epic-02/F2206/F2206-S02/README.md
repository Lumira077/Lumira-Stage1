# F2206-S02

Jira: https://lumira077.atlassian.net/browse/KR1-50

- 2개 가상 Provider 어댑터 및 공통 응답 검증·예산 초과·오류 정규화 구현
- Gateway 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 2개 이상 실제 Provider를 동일 계약으로 호출하고 인증정보를 로그/기기에 노출하지 않으며 모델 교체 시 상위 로직 변경이 없다.

현재 제한: 현재는 가상 Provider 2개만 연결; 실제 서비스 계정·모델·Secret·호출 한도·네트워크 어댑터 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
