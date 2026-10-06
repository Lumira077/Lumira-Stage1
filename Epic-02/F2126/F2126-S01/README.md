# F2126-S01

Jira: https://lumira077.atlassian.net/browse/KR1-139

- 마이크 geometry·channel/order·PCM/sample-rate/frame·TTS loopback·clock/delay·AEC/DOA 기준 정의
- AudioFrame: channels, reference, sample_rate, timestamp; DOA: spacing_m, delay_samples, confidence, calibration_version의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- AudioLab.beam/subtract_reference/doa; 실제 adaptive AEC·beamformer는 WebRTC/승인 DSP adapter의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 실제 TTS 재생·잡음·거리/방향 조건에서 AEC/DOA/STT 품질 목표를 충족하며 DOA를 사용자 인증으로 사용하지 않는다.

현재 제한: 현재 기초 DSP 계산·계약 시험. adaptive AEC·실제 beamformer·TDOA 추정·마이크 배열·실물 성능 미구현

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
