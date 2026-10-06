# F2011-S01

Jira: https://lumira077.atlassian.net/browse/KR1-104

- 세션·turn·epoch·history 상한·TTL·저장 동의·요약 시점·F2003 장기 기억 분리 정의
- Session: actor, epoch, expires_at, history, finalized_turns; transient history와 durable memory 분리의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- ConversationSession.open/check/append/switch/cancel; F2004/F2003 운영 이벤트와 결합의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 사용자 간 문맥 노출 0건, 정해진 상한 유지, 삭제·취소된 세션의 늦은 응답 폐기.

현재 제한: 현재 단일 프로세스 일시 메모리; 인증·분산 세션·durable 요약·자동 동의 이벤트 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
