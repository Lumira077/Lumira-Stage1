# F2207-S04

Jira: https://lumira077.atlassian.net/browse/KR1-57

- 음성/영상 timestamp 차이, 영상 차단율·전송량·재연결 시간의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- 시각 문맥이 꼭 필요한 요청에만 동의된 음성·영상·텍스트의 Cloud 실시간 세션을 연다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 실제 음성·영상의 시각 동기화와 종료·재연결을 확인하고 필요 없는 영상 전송을 차단한다.

현재 제한: 실제 WebRTC/WebSocket·카메라·마이크·영상/음성 동의 UI·시각 모델 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
