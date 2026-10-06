# F2123-S01

Jira: https://lumira077.atlassian.net/browse/KR1-134

- F2205 정책 권위와 F2123 실행 orchestration 책임을 분리하고 하위 모듈 순서/일관 snapshot 정의
- RoutePacket: decision, policy/consent/price_version, epoch, budget_state, network_state, reason_codes의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- HybridRouter.route(RouteInput,snapshot) → packet; F2010/F2206 소비자가 호출 직전 재검증의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 대표 Case별 사유가 기록되고 개인화·품질·비용·프라이버시·안전 기준을 함께 충족한다.

현재 제한: 현재 신뢰된 상태 snapshot의 로컬 조합; 실시간 분산 이벤트·actual Cloud/Local·요금제·운영 개인화 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
