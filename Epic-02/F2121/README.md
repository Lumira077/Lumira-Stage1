# [F2121] Stage1 오프라인 기본 명령·Local 안전 응답

Jira: https://lumira077.atlassian.net/browse/KR1-123

네트워크에 의존하지 않는 호출·정지·상태·프라이버시 기본 명령을 Local에서 처리한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `LocalCommands`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 6개 합성 입력 시험.

제약: 현재 정확 문구 parser와 proposal. 실제 제어·삭제·긴급 연락·물리 안전 경로 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [F2021 감정형 TTS 연동](https://lumira077.atlassian.net/browse/KR1-175) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
