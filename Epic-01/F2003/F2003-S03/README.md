# F2003-S03 통합·품질·성능·안전 시험

[Jira KR1-15](https://lumira077.atlassian.net/browse/KR1-15)

```sh
python -c "import memory_lab; import unittest; unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))"
# 전체 품질/성능: S04에서 python -m memory_ops.runner --out results --samples 100
```

Dialogue.prepare는 원문 없는 ticket, respond는 private_output_confirmed:true와 최신 정책 확인 후 구조화 reference만 반환한다. TTS/표현/제어 dispatch:false, executable_actions:[]이다. 모델·검색 장애 safe_prepare fallback은 빈 기억으로 반환하며 회상을 만들어내지 않는다.

고정 evaluation-set.json: 합성18발화(긍정8/비후보10)의 후보 precision/recall·내용 일치, 검색4사례의 top1 accuracy/틀린 기억 반환률. 정답·데이터 SHA·규칙/검색 버전을 quality.json에 기록한다. 외부 LLM·음성/얼굴 인식·의미 임베딩·실제 사용자 대화를 평가하지 않았다. 제한된 패턴 탐지가 모든 민감정보·프롬프트 공격을 차단한다는 증거가 아니다.

다섯 경로 추출/후보 저장/검색/context 준비/context 반환을 각각100회 측정한다. 확인 기억100개/짧은 합성문자열의 SQLite in-process 환경이다. p50/p95/max/실패율·대상개수·실행환경을 기록하고 로컬 초기 제안p95≤500ms와 비교한다. 실제 모델·클라우드·STT/TTS·물리 동작 지연은 제외된다.

실기 필수: 실제 활성 사용자·보호자·게스트 권한, 제3자 앞 기억 발화, TTS·표현 안전, 실제 모델의 지시/누출 공격, 소음/인식오류, 네트워크·전원·장치 안전정지, 다중 DB/외부 캐시·삭제/철회 시점 일관성. 모의 성공으로 완료하지 않는다.
