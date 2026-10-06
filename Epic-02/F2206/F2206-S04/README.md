# F2206-S04

Jira: https://lumira077.atlassian.net/browse/KR1-52

- Provider별 성공률·첫 응답/완료 지연·usage 누락률·rate limit·비용의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- Provider 차이를 공통 요청·응답·오류·사용량 계약으로 감싸 상위 대화 로직 변경을 줄인다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 2개 이상 실제 Provider를 동일 계약으로 호출하고 인증정보를 로그/기기에 노출하지 않으며 모델 교체 시 상위 로직 변경이 없다.

현재 제한: 현재는 가상 Provider 2개만 연결; 실제 서비스 계정·모델·Secret·호출 한도·네트워크 어댑터 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
