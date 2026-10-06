# F2212-S01

Jira: https://lumira077.atlassian.net/browse/KR1-79

- 429/5xx/timeout/auth 오류·부분 출력·retry-after·deadline·대체 Provider 승인 규칙 정의
- Attempt: turn_id, epoch, provider, failure_class, emitted; Recovery: chosen_backend, attempts, final_state의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- Recovery.complete(ordered_adapters,turn); 각 호출 전 F2211·F2209 재확인, 실제 stream 복구는 별도의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 원인과 attempt를 기록하고 목표 복구시간 내 전환하며 동일 turn의 최종 출력이 중복되지 않는다.

현재 제한: 실제 Provider retry/circuit breaker·stream cancellation·timeout 제어·부분 오디오 복귀 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
