# F2009-S04

Jira: https://lumira077.atlassian.net/browse/KR1-97

- CER/WER·partial/final p95·endpoint 지연·무음 오인식의 모니터링·알람·데이터 보존·복귀 기준을 수립한다.
- STT 부분 결과와 확정 결과를 순서대로 관리하고 확정된 발화만 대화 처리에 넘긴다.의 실제 사용자 시나리오를 평가하고 실제 참가자 수·피드백·언어/환경을 기록한다.
- source/model/prompt/policy/asset/config version·Secret 참조·Q1 시험 검토·R1 승인·rollback 증적을 Release Manifest로 연결한다.

산출물: 지표/사용자 평가 계획·Release assessment·배포/복귀 runbook

상위 Feature 완료조건: 환경/언어별 CER/WER와 partial/final 지연 목표를 충족하고 확정 결과가 중복 처리되지 않는다.

현재 제한: 현재 전사 이벤트 조립기; 음성→텍스트 모델·VAD·실녹음 평가 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
