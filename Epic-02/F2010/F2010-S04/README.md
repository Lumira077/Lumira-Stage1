# F2010-S04

Jira: https://lumira077.atlassian.net/browse/KR1-102

- 응답 적합성·문맥 유지·first token/end-to-end p95·중복/위험 출력의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- 현재 사용자 Context와 정책에 맞는 LLM 응답을 생성하고 출력 전 검증한다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 실제 다중 Provider에서 문맥이 유지되고 모델별 지연·비용·실패·안전 출력 증적이 남는다.

현재 제한: 현재 고정 응답 가상 Gateway 통합; 실제 자연어 생성·prompt 평가·TTS·기억/콘텐츠 Tool 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
