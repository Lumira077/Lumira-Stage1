# F2207-S01

Jira: https://lumira077.atlassian.net/browse/KR1-54

- 세션 open/active/reconnecting/closed 및 media 동의·sample-rate·timestamp·backpressure 계약 작성
- RealtimeSession: session_id, epoch, media_consent, visual_needed, frame_seq, state; frame 원문은 기본 미저장의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- RealtimeGate.accept(modality,seq,epoch); 실제 transport는 승인된 Realtime/Live 어댑터의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 실제 음성·영상의 시각 동기화와 종료·재연결을 확인하고 필요 없는 영상 전송을 차단한다.

현재 제한: 실제 WebRTC/WebSocket·카메라·마이크·영상/음성 동의 UI·시각 모델 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
