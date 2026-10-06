# F2211-S04

Jira: https://lumira077.atlassian.net/browse/KR1-77

- 금지 전송 0건·분류 오누락·동의 철회 반영 지연·reason 분포의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- 민감도·동의·안전 등급에 따라 전송 금지 및 승인 Provider 경계를 강제한다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 승인된 시험 집합에서 금지 전송 0건이며 policy/consent version이 감사 메타데이터에 남는다.

현재 제한: 분류 등급은 신뢰된 호출자 입력. 실제 PII 탐지·동의 이벤트·완전한 익명화·전송 감사 미구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
