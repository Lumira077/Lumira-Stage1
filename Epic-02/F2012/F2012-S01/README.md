# F2012-S01

Jira: https://lumira077.atlassian.net/browse/KR1-109

- VAD barge-in·TTS echo·우선순위·취소 ACK·playback 위치·모드 전환 계약 정의
- CancelRequest: turn_id, epoch, modules; Ack: module, cancelled_epoch, playback_position, status의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- InterruptController.cancel/ack/accept_output; F2021·로봇 소비자에서 실제 취소 ACK 필요의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 실기 TTS/동작 취소 지연 목표와 미취소 출력 0건을 충족하고 ACK 누락 시 재개하지 않는다.

현재 제한: 현재 메타데이터 취소 요청/ACK; 실제 마이크 VAD·TTS/모터 큐·안전 정지 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
