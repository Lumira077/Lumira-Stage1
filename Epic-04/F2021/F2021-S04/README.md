# F2021-S04

Jira: https://lumira077.atlassian.net/browse/KR1-179

사용자 voice 선호/정정·조용한 모드·접근성·캐시 삭제·provider 장애 local fallback/rollback을 검토한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: first audio/p50/p95·MOS/명료도·언어/style 지원·audio underrun·취소 잔여재생·Cloud 미동의 전송 0건

제한: 실제 TTS/voice weights/Provider·스피커/driver/playback·alignment·emotion prosody 품질·캐시·AEC reference 미연결. demo voice/style는 API 계획 fixture이다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
