# [F2157] 의상 연동 Persona Theme 전환

Jira: https://lumira077.atlassian.net/browse/KR1-37

NFC 의상 식별을 기반으로 얼굴 스킨·음성·동작·대화 콘텐츠의 Persona Theme를 함께 바꾼다. 의상 오류·제거·사용자 제한에서는 기본 Persona로 복귀한다.

실행: 저장소 루트에서 `python Epic-01/integration/run.py`. Python 3.11 이상, 표준 라이브러리만 사용.

이 패키지는 **개발용 로컬 Prototype**이다. 실제 인증, 생체 식별, LLM/STT/TTS, NFC 센서, 로봇 출력, 운영 승인과 실사용 평가가 연결되지 않아 S03 실기 통합 및 S04 Release 완료를 주장하지 않는다.
