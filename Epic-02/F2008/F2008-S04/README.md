# F2008-S04

Jira: https://lumira077.atlassian.net/browse/KR1-92

- FAR/시간·FRR·wake 지연·중복 세션 0건의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- 호출어 감지 결과를 검증하여 대화 시작을 한 번 허용하고 중복/에코 오호출을 줄인다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 실기 호출·비호출 데이터에서 승인된 FAR/FRR와 지연을 충족하고 mute/에코로 세션이 시작되지 않는다.

현재 제한: 현재 detector score 입력 gate만 구현; 실제 wakeword 모델·발음 학습·마이크·AEC 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
