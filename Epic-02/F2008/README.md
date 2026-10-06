# [F2008] 호출어 및 대화 시작

Jira: https://lumira077.atlassian.net/browse/KR1-88

호출어 감지 결과를 검증하여 대화 시작을 한 번 허용하고 중복/에코 오호출을 줄인다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `WakeGate`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 7개 합성 입력 시험.

제약: 현재 detector score 입력 gate만 구현; 실제 wakeword 모델·발음 학습·마이크·AEC 필요

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [whisper.cpp 소스](https://github.com/ggml-org/whisper.cpp) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [WebRTC Audio Processing 소스](https://webrtc.googlesource.com/src/+/refs/heads/main/modules/audio_processing/) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
