# [F2123] Stage3 Hybrid AI Router 및 개인화

Jira: https://lumira077.atlassian.net/browse/KR1-133

통합 Router가 정책·프라이버시·예산·네트워크·Context를 조합해 설명 가능한 경로를 선택한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `HybridRouter`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 7개 합성 입력 시험.

제약: 현재 신뢰된 상태 snapshot의 로컬 조합; 실시간 분산 이벤트·actual Cloud/Local·요금제·운영 개인화 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [Epic-01 개인화·동의](https://lumira077.atlassian.net/browse/KR1-1) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [OpenAI Realtime 공식 문서](https://developers.openai.com/api/docs/guides/realtime) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [Gemini Live 공식 문서](https://ai.google.dev/gemini-api/docs/live-api) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
