# [F2009] 실시간 음성 인식(STT)

Jira: https://lumira077.atlassian.net/browse/KR1-93

STT 부분 결과와 확정 결과를 순서대로 관리하고 확정된 발화만 대화 처리에 넘긴다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `TranscriptAssembler`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 6개 합성 입력 시험.

제약: 현재 전사 이벤트 조립기; 음성→텍스트 모델·VAD·실녹음 평가 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [whisper.cpp 소스](https://github.com/ggml-org/whisper.cpp) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [WebRTC Audio Processing 소스](https://webrtc.googlesource.com/src/+/refs/heads/main/modules/audio_processing/) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
