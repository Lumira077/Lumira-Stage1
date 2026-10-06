# F2129-S02

Jira: https://lumira077.atlassian.net/browse/KR1-202

현재 SkinRegistry는 id/version/color/6개 필수 state/rights 및 실제 canonical JSON SHA256을 검증하고 검증 완료 후 메모리에서 원자적으로 교체한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: skin 전환 p95·FPS/memory·상태 의미 일치/이해율·변조/누락 fallback·권리 증거·접근성

제한: 2.5D/texture/sprite/shader·persona event/실제 theme asset·장비 FPS·rights 증거/OTA 서명 미구현. 메모리 atomic metadata switch만 구현한 개발 Prototype이다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
