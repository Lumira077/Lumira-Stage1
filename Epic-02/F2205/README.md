# [F2205] Hybrid AI Policy Engine

Jira: https://lumira077.atlassian.net/browse/KR1-43

대화 목적·민감도·안전·지연·네트워크·요금제·로봇 상태를 결정적 정책으로 평가한다.

## 실행·현재 수행 범위

저장소 루트에서 `python Epic-02/runtime/run.py`. Python 3.11 이상, 표준 라이브러리만 사용한다.

S02 entrypoint는 `implementation.py`의 `PolicyEngine`다. 공통 안전·세션 계약을 중복하지 않기 위해 실제 로직은 `Epic-02/runtime/core.py`에 있다. `python Epic-02/runtime/demo.py`는 가상 Provider 기반 통합 예시다.

현재 범위: 개발용 핵심 계약·로컬 Prototype, 8개 합성 입력 시험.

제약: 실제 위험 분류기·운영 정책 승인·실시간 로봇/요금제 상태 미연결

실기·모델 품질·실사용·운영 승인 미완료이므로 Feature 완료 또는 Release를 주장하지 않는다.

## 연동 도구
- [Epic-01 개인화·동의](https://lumira077.atlassian.net/browse/KR1-1) — 참조/후속 연동; 현재 서비스 연결을 뜻하지 않음
