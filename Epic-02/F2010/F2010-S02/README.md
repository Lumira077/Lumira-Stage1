# F2010-S02

Jira: https://lumira077.atlassian.net/browse/KR1-100

- F2205/F2211 경로 판단·F2206/F2212 응답·F2014 출력 정책을 결합하는 대화 orchestrator 구현
- Dialogue 로컬 핵심 로직과 재현 가능한 fixture·자동 시험을 구현하고 실제 adapter와 fake adapter를 구분한다.
- 동일 입력 재현·유한 숫자/크기/상태 검증·예외 시 안전 경로를 구현한다. 필요한 계정·장비는 linked Tool manifest에 미연결로 표시한다.

산출물: 로컬 Prototype entrypoint·공통 runtime·합성 fixture·실행 안내

상위 Feature 완료조건: 실제 다중 Provider에서 문맥이 유지되고 모델별 지연·비용·실패·안전 출력 증적이 남는다.

현재 제한: 현재 고정 응답 가상 Gateway 통합; 실제 자연어 생성·prompt 평가·TTS·기억/콘텐츠 Tool 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
