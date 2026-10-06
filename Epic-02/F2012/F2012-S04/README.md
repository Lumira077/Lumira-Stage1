# F2012-S04

Jira: https://lumira077.atlassian.net/browse/KR1-112

- barge-in/stop→실제 무음/정지 p95·미확인 ACK·late drop의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- 사용자 발화/정지 시 생성·TTS·표정·동작의 동일 turn 출력을 중단한다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 실기 TTS/동작 취소 지연 목표와 미취소 출력 0건을 충족하고 ACK 누락 시 재개하지 않는다.

현재 제한: 현재 메타데이터 취소 요청/ACK; 실제 마이크 VAD·TTS/모터 큐·안전 정지 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
