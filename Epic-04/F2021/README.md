# [F2021] 감정형 TTS 음성 출력

Jira: https://lumira077.atlassian.net/browse/KR1-175

음성 persona와 감정 스타일·속도·음량을 조절해 명료한 대화 음성을 출력하고 끼어들기/조용한 모드를 반영한다.

bounded text·locale·voice/model/hash/license·supported style·rate/volume·sample rate·audio duration/word/viseme timestamps·turn/epoch·cancel token·Cloud 동의.

F2010 대화 출력 → 안전/동의/voice locale 검사 → TTS adapter → playback ACK/reference audio → F2126 AEC/F2023 타임라인/F2130 립싱크. 현재 audio 합성/재생 미연결.

## 단계별 개발
- voice/언어/style 지원 표·텍스트 정규화·quiet/volume·Cloud 전송/캐시 보존·chunk/cancel/alignment 계약을 설계한다.
- 현재 TTSPlanner는 demo-ko/demo-en fixture voice·locale·길이/rate/volume·style fallback/quiet/Cloud 동의의 계획을 생성한다. 음성 합성 없이 characters metadata만 반환한다.
- 실제 TTS first audio/p95·명료도/자연성·지원 language/style·끊김/취소 ACK·잔여 재생·AEC reference를 검증한다.
- 사용자 voice 선호/정정·조용한 모드·접근성·캐시 삭제·provider 장애 local fallback/rollback을 검토한다.

## 검증·제한

first audio/p50/p95·MOS/명료도·언어/style 지원·audio underrun·취소 잔여재생·Cloud 미동의 전송 0건

실제 TTS/voice weights/Provider·스피커/driver/playback·alignment·emotion prosody 품질·캐시·AEC reference 미연결. demo voice/style는 API 계획 fixture이다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 9개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [Piper current repository (runtime/voice 라이선스·한국어/style 검토 필요)](https://github.com/OHF-Voice/piper1-gpl) — 후속 후보; 미설치/미연결.
