# F2008-S01

Jira: https://lumira077.atlassian.net/browse/KR1-89

- 호출어·감지 score·마이크 mute·TTS echo·cooldown·manual start·timeout 조건 정의
- WakeEvent: event_id, score, detected_at, epoch, audio_source; WakeState: ready/listening/cooldown의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- WakeGate.trigger(event) → accepted/start_session; 실제 wake model은 별도 adapter의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 실기 호출·비호출 데이터에서 승인된 FAR/FRR와 지연을 충족하고 mute/에코로 세션이 시작되지 않는다.

현재 제한: 현재 detector score 입력 gate만 구현; 실제 wakeword 모델·발음 학습·마이크·AEC 필요

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
