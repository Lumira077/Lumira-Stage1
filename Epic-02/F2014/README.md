# [F2014] 연령·상황별 안전 대화 정책

Jira: https://lumira077.atlassian.net/browse/KR1-118

연령·상황·위험 태그에 따라 안전한 응답 범위와 위기 안내를 적용한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `SafetyPolicy`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 7개 합성 입력 시험.

제약: 현재 태그 기반 정책 gate; 실제 의미 분류·유해성 검출·전문가 검토·긴급 연락 서비스 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [Epic-01 개인화·동의](https://lumira077.atlassian.net/browse/KR1-1) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [F2021 감정형 TTS 연동](https://lumira077.atlassian.net/browse/KR1-175) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
