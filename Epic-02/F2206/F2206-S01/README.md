# F2206-S01

Jira: https://lumira077.atlassian.net/browse/KR1-49

- Provider별 request/model/stream/cancel/usage/error 매핑과 key 보관·allowlist·timeout 계약 작성
- Request: request_id, turn_id, epoch, model, max_output; Response: provider, text, usage_tokens, status; credentials는 Secret 참조만의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- Gateway.complete(provider,request) → NormalizedResponse; 운영 stream/cancel은 별도 어댑터 인터페이스의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 2개 이상 실제 Provider를 동일 계약으로 호출하고 인증정보를 로그/기기에 노출하지 않으며 모델 교체 시 상위 로직 변경이 없다.

현재 제한: 현재는 가상 Provider 2개만 연결; 실제 서비스 계정·모델·Secret·호출 한도·네트워크 어댑터 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
