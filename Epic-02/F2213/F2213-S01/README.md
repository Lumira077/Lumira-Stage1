# F2213-S01

Jira: https://lumira077.atlassian.net/browse/KR1-84

- 이벤트 allowlist·토큰/credit 단위·sampling/retention·사용자 피드백 별도 동의 정의
- Telemetry: provider_code, status, latency_ms, usage_tokens, cost_units; conversation/user/secret 문자열 제외의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- QualityTelemetry.record/snapshot; 운영 F2079/F2080 원가·F2205 정책 버전 참조의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: Provider·모델·요금제별 대시보드가 운영 데이터로 검증되며 민감 로그와 추정 비용을 분리한다.

현재 제한: 현재 메모리 집계와 JSON report; 실제 metrics backend·대시보드·보존/삭제·청구 데이터 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
