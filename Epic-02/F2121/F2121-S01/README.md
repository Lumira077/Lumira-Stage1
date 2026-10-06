# F2121-S01

Jira: https://lumira077.atlassian.net/browse/KR1-124

- 정확한 로컬 명령 문구·권한·stop 우선·위기 안내와 실제 연락/삭제 구분 정의
- LocalCommand: intent, action_id, required_authority; Result: proposal_only, message, executed의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- LocalCommands.parse(text) → proposal; 실제 stop은 별도 안전 제어기로 즉시 전달·ACK의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 실기 기본 명령이 Cloud 호출 없이 목표시간 내 수행되고 긴급 연락/삭제는 실제 실행 증거 없이 완료로 응답하지 않는다.

현재 제한: 현재 정확 문구 parser와 proposal. 실제 제어·삭제·긴급 연락·물리 안전 경로 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
