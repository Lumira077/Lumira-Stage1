# F2211-S01

Jira: https://lumira077.atlassian.net/browse/KR1-74

- public/personal/sensitive/unknown 등급, Cloud 동의·Provider allowlist·안전 local-only 규칙 정의
- PrivacyDecision: allow_cloud, local_only, reason, consent_revision, approved_provider; raw content 분류 결과 별도의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- PrivacyGuard.check(classification,consent,safety,provider) → decision; F2205/F2206/F2207 호출 직전 재평가의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 승인된 시험 집합에서 금지 전송 0건이며 policy/consent version이 감사 메타데이터에 남는다.

현재 제한: 분류 등급은 신뢰된 호출자 입력. 실제 PII 탐지·동의 이벤트·완전한 익명화·전송 감사 미구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
