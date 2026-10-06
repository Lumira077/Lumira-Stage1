# F2209-S01

Jira: https://lumira077.atlassian.net/browse/KR1-64

- F2079/F2080 권위 원가·요금제 인터페이스와 원가/과금 credit 분리·단위·가격 버전 정의
- Budget: available_units, reserved_units, price_version; Reservation: request_id, max_units, actual_units, state의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- Budget.reserve/settle/cancel; 운영 요금제 서비스의 계정별 원자적 예약 계약의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 동시 요청에도 한도를 넘지 않고 미확인 사용량을 0원으로 확정하지 않으며 가격 버전을 기록한다.

현재 제한: 단일 프로세스 메모리 ledger. 실제 F2079/F2080·분산 원장·Provider usage·가격/환율·청구 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
