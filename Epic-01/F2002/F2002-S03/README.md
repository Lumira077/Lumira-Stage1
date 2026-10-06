# F2002-S03 로봇 통합·성능·안전 시험

[Jira KR1-10](https://lumira077.atlassian.net/browse/KR1-10)

```sh
python -c "import profile_lab; import unittest; unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))"
# 저장/적용 각각 100회 지연 측정은 S04 runner로 수행
```

5개 모듈 dialogue/recognition/tts/expression/control을 모의 설정 수신기로 연결한다. 테스트: 전체 ACK, 중복 없는 재적용, 부분 실패 후 재시도, 프로세스 재생성 후 ACK 보존, 잘못된 ACK 거부, 동의 철회 후 stale context 차단, 모의 cap, 음소거·제스처 off, 단절·삭제·다른 actor 차단, ACK 원문 제외, F2001 실제 서비스 코드의 등록→프로필 가져오기.

실제 로봇 연결 없음. 모의 설정 일치성은 실제 음성/인식 정확도가 아니다. 시간 측정은 SQLite와 in-process ACK의 ms이며 네트워크·발화 시작·모터 동작을 포함하지 않는다. 제안 성능 기준 p95 저장≤500ms/적용≤1000ms는 실기 수용 기준이 아니며 대상 장치에서 확정해야 한다. 장치 cap 40/2/1은 제안 표현 단계이며 물리 안전 범위를 의미하지 않는다.

실기 필수: 실제 소유권·사용자 전환, STT/TTS 호칭·언어·음량·속도, 인식 동의 차단, 디스플레이 표정·제스처, 관절 제한·정지·기종별 출력 한계, 네트워크/전원/제어기 장애 복귀, 원격 ACK 중복·순서·시간초과, 삭제/철회 후 캐시 무효화. Q1/R1 검토 증적 필요.
