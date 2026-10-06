# F2009-S01

Jira: https://lumira077.atlassian.net/browse/KR1-94

- PCM/sample-rate/channels·VAD·partial/final·언어·sequence·취소 계약 정의
- Transcript: utterance_id, sequence, text, is_final, language, epoch; audio bytes는 기본 미저장의 필수값·민감도·보존기간·권한·revision/epoch를 표로 정의한다.
- TranscriptAssembler.update/final; 실제 whisper.cpp 또는 승인 STT adapter를 연결의 정상·오류·취소·stale 입력 계약 및 시험 데이터 분할을 명세화한다.

산출물: 요구사항·데이터/인터페이스 계약·예외표·시험 기준

상위 Feature 완료조건: 환경/언어별 CER/WER와 partial/final 지연 목표를 충족하고 확정 결과가 중복 처리되지 않는다.

현재 제한: 현재 전사 이벤트 조립기; 음성→텍스트 모델·VAD·실녹음 평가 미연결

S03 실기 시험·S04 실제 사용자 평가/운영 승인은 미실시. 숫자 목표는 승인 후 시험 계약에 version과 함께 등록한다.
