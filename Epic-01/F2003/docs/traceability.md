# KR1-12 / F2003 요구사항 추적

| 단계 | 소스·개발 증적 | 실제 추가 완료조건 |
|---|---|---|
| S01 KR1-13 | memory_contract, design/openapi, 입력/정책/규칙19시험 | 실제 모델/저장/인증/보존/품질 기준 설계 승인 |
| S02 KR1-14 | memory_service, CRUD/동의/인덱스/HTTP/멱등31시험 | 운영 인증·암호화·consent epoch·분산 원자성·벡터/클라우드 동기화 |
| S03 KR1-15 | memory_lab, context/장애13시험, 고정18발화·검색4사례, 5경로100회 | 실제 LLM·모델 품질·STT/TTS·표현/제어·물리 안전·대규모 부하 |
| S04 KR1-16 | memory_ops, 지표/원장/복원20시험, Dashboard·Release gate | 실제 사용자·운영 기준·배포/복귀·원장 진위·Q1/R1 승인 |

합계83개 자동 시험. 소프트웨어 시험/합성 품질100%는 해당 fixture만의 결과이며 일반 대화의 품질·보안 완료 근거가 아니다. 실제 참가자0, hardware/model/cloud not_run, Release blocked. CI는 F2001/F2002 회귀를 함께 수행하고 결과는30일 Artifact에 보관한다. 실제 장기 증적은 승인된 보호 저장소에 보관해 Jira에 링크한다.
