# [F2013] 다국어 대화

Jira: https://lumira077.atlassian.net/browse/KR1-113

STT·대화·TTS·콘텐츠의 지원 언어를 함께 검증하고 사용자 선택을 우선한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `LanguageResolver`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 6개 합성 입력 시험.

제약: 현재 한영 locale 지원 계약만 구현; 실제 다국어 모델·번역/언어 감지·음성 품질 평가 필요

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [whisper.cpp 소스](https://github.com/ggml-org/whisper.cpp) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [F2021 감정형 TTS 연동](https://lumira077.atlassian.net/browse/KR1-175) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
- [Epic-01 개인화·동의](https://lumira077.atlassian.net/browse/KR1-1) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
