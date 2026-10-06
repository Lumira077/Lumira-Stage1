# [F2004] 다중 사용자 및 가족 식별

Jira: https://lumira077.atlassian.net/browse/KR1-17

여러 가족이 한 로봇을 사용할 때 현재 대화 사용자를 확인하고 각자의 프로필·기억을 분리한다. 식별이 불확실하면 개인 정보를 사용하지 않는 게스트 경로로 전환한다.

실행: 저장소 루트에서 `python Epic-01/integration/run.py`. Python 3.11 이상, 표준 라이브러리만 사용.

이 패키지는 **개발용 로컬 Prototype**이다. 실제 인증, 생체 식별, LLM/STT/TTS, NFC 센서, 로봇 출력, 운영 승인과 실사용 평가가 연결되지 않아 S03 실기 통합 및 S04 Release 완료를 주장하지 않는다.
