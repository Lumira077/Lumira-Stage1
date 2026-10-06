# F2212-S03

Jira: https://lumira077.atlassian.net/browse/KR1-81

- provider 장애·모든 Provider 실패·local fallback·늦은 응답·이미 출력된 turn 시험
- 운영 품질지표: 복구 시간·대체율·중복 출력 0건·auth/429 오류·circuit 상태. 장비·모델·설정·sample·기대/실제 결과·결함/재시험을 묶어 증적화한다.
- 실제 장치의 지연·정확도·안전·취소·실패 복구를 검증하고 시뮬레이션 합격과 구분한다. 개인정보 노출·금지 전송/출력은 시험 집합에서 0건이어야 한다.

산출물: 자동 시험 소스·CI report·실기 평가표·결함/재시험 증적

상위 Feature 완료조건: 원인과 attempt를 기록하고 목표 복구시간 내 전환하며 동일 turn의 최종 출력이 중복되지 않는다.

현재 제한: 실제 Provider retry/circuit breaker·stream cancellation·timeout 제어·부분 오디오 복귀 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
