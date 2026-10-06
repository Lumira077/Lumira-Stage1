# [F2129] 2D·2.5D Character Face Engine 및 Persona Skin

Jira: https://lumira077.atlassian.net/browse/KR1-200

Stage 1 캐릭터 2D/2.5D 얼굴 엔진과 고객군별 Persona Skin을 공통 의미 상태로 전환하고 실패 시 기존 스킨을 유지한다.

skin id/version·palette·semantic states·asset hash/rights·persona/profile mapping·resolution/FPS/memory·default skin·activation/rollback.

asset manifest validation/hash → atomic active skin snapshot → F2020 renderer. F2002 persona와 선택 계약; 현재 renderer bundle schema는 color/state metadata만 다룬다.

## 단계별 개발
- 공통 표정/상태 의미·테마/asset registry·권리/hash·resolution/performance·atomic switch/fallback·persona 매핑을 설계한다.
- 현재 SkinRegistry는 id/version/color/6개 필수 state/rights 및 실제 canonical JSON SHA256을 검증하고 검증 완료 후 메모리에서 원자적으로 교체한다.
- 실제 sprite/vector/2.5D shader renderer·스킨 전환 후 의미 일치·누락/변조/권한/메모리·FPS·rollback을 시험한다.
- Elder/Home/Kids/Hospital/Pet별 상태 이해/선호·접근성·asset rights·콘텐츠 검토/배포를 확정한다.

## 검증·제한

skin 전환 p95·FPS/memory·상태 의미 일치/이해율·변조/누락 fallback·권리 증거·접근성

2.5D/texture/sprite/shader·persona event/실제 theme asset·장비 FPS·rights 증거/OTA 서명 미구현. 메모리 atomic metadata switch만 구현한 개발 Prototype이다.

S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

실행: 저장소 루트 `python Epic-04/runtime/run.py`. Python 3.11+, 표준 라이브러리만 사용. S02는 공통 runtime/core.py의 entrypoint. 8개 합성 입력 시험. 실제 TTS/디스플레이/모터/참가자/운영 배포 없음. 신뢰된 호출자가 owner/consent/clearance/rights/intent를 공급한다; 실제 인증·환경/권리/의미 검증 서비스가 아니다.

도구 참조: [Qt Quick (후속 renderer 후보)](https://doc.qt.io/qt-6/qtquick-index.html) — 후속 후보; 미설치/미연결.
