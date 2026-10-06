# [F2122] Stage2 Small Local LLM·RAG·NPU 실행

Jira: https://lumira077.atlassian.net/browse/KR1-128

Edge Local LLM/RAG의 실행 조건과 자원 상한을 검증하고 승인된 Tool만 제안하게 한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `LocalModelGate`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 7개 합성 입력 시험.

제약: 현재 자원/Tool gate만 구현; 모델 다운로드·실제 추론·RK3588 NPU/Jetson 가속·실물 benchmark 미실시

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [llama.cpp 소스](https://github.com/ggml-org/llama.cpp) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [RKNN Toolkit2 소스](https://github.com/rockchip-linux/rknn-toolkit2) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
