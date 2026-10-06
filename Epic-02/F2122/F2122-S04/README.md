# F2122-S04

Jira: https://lumira077.atlassian.net/browse/KR1-132

- peak RAM·tokens/s·TTFT·온도/전력·fallback·Tool 거절의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- Edge Local LLM/RAG의 실행 조건과 자원 상한을 검증하고 승인된 Tool만 제안하게 한다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 선정 모델을 실제 보드에서 실행해 RAM/first token/속도/발열 목표와 승인 Tool 검증을 통과한다.

현재 제한: 현재 자원/Tool gate만 구현; 모델 다운로드·실제 추론·RK3588 NPU/Jetson 가속·실물 benchmark 미실시

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
