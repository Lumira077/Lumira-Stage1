# F2210-S01

Jira: https://lumira077.atlassian.net/browse/KR1-69

- RTT/loss/bandwidth/측정시각·유효기간 및 단절·회복 조건 정의
- NetworkSample: rtt_ms, loss_ratio, bandwidth_kbps, measured_at; RouteHealth: local/cloud, recovery_count의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- NetworkMonitor.observe(sample) → routing_hint; 실제 측정은 네트워크 어댑터의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 정의된 열화 시험에서 개인정보/세션을 보존하며 대체 경로로 전환하고 회복 시 반복 재접속을 방지한다.

현재 제한: 현재 합성 측정 입력; 실제 probe·장치 Wi-Fi/LTE·전환 성능 미실측

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
