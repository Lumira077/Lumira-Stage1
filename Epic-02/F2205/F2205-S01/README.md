# F2205-S01

Jira: https://lumira077.atlassian.net/browse/KR1-44

- stop/안전 명령 → 개인정보·동의 → 로봇 상태 → 네트워크·credit → 시각 필요·복잡도 순의 우선순위표 작성
- RouteInput: purpose, sensitivity, safety_command, cloud_consent, visual_needed, network_ok, credits, robot_ready; Decision: route, reason, policy_version의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- PolicyEngine.decide(RouteInput) → Decision; 실행과 과금은 하지 않는 정책 판단 계약의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 동일 입력에 동일 경로/사유를 반환하고 개인정보·안전 금지 조건이 비용/품질 선호에 의해 완화되지 않는다.

현재 제한: 실제 위험 분류기·운영 정책 승인·실시간 로봇/요금제 상태 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
