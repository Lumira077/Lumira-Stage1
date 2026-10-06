# [F2206] Multi-Cloud LLM Gateway

Jira: https://lumira077.atlassian.net/browse/KR1-48

Provider 차이를 공통 요청·응답·오류·사용량 계약으로 감싸 상위 대화 로직 변경을 줄인다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `Gateway`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 6개 합성 입력 시험.

제약: 현재는 가상 Provider 2개만 연결; 실제 서비스 계정·모델·Secret·호출 한도·네트워크 어댑터 필요

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [OpenAI Realtime 공식 문서](https://developers.openai.com/api/docs/guides/realtime) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [Gemini Live 공식 문서](https://ai.google.dev/gemini-api/docs/live-api) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
