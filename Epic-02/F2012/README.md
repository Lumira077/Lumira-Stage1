# [F2012] 대화 중 끼어들기와 중단

Jira: https://lumira077.atlassian.net/browse/KR1-108

사용자 발화/정지 시 생성·TTS·표정·동작의 동일 turn 출력을 중단한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `InterruptController`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 6개 합성 입력 시험.

제약: 현재 메타데이터 취소 요청/ACK; 실제 마이크 VAD·TTS/모터 큐·안전 정지 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [F2021 감정형 TTS 연동](https://lumira077.atlassian.net/browse/KR1-175) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [WebRTC Audio Processing 소스](https://webrtc.googlesource.com/src/+/refs/heads/main/modules/audio_processing/) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
