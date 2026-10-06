# [F2212] LLM Failover 및 Session Recovery

Jira: https://lumira077.atlassian.net/browse/KR1-78

Provider 장애 시 허용된 대체 경로로 전환하며 이미 출력한 답변과 중복되지 않게 한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `Recovery`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 6개 합성 입력 시험.

제약: 실제 Provider retry/circuit breaker·stream cancellation·timeout 제어·부분 오디오 복귀 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [OpenAI Realtime 공식 문서](https://developers.openai.com/api/docs/guides/realtime) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [Gemini Live 공식 문서](https://ai.google.dev/gemini-api/docs/live-api) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
