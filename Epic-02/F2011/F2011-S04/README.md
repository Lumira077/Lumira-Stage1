# F2011-S04

Jira: https://lumira077.atlassian.net/browse/KR1-107

- 노출 0건·history 크기·TTL 정리·Context hit·stale drop의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- 짧은 대화 문맥을 사용자별 격리하고 전환·종료·TTL·취소 시 폐기한다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 사용자 간 문맥 노출 0건, 정해진 상한 유지, 삭제·취소된 세션의 늦은 응답 폐기.

현재 제한: 현재 단일 프로세스 일시 메모리; 인증·분산 세션·durable 요약·자동 동의 이벤트 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
