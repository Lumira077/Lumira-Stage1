# F2130-S04

Jira: https://lumira077.atlassian.net/browse/KR1-209

과도한 응시/입모양 불편·눈 피로·접근성·camera 동의 및 alignment/asset rollback을 검토한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: lip/audio skew p95·gaze error·blink 자연성·missing cue fallback·취소 residual·사용자 불편

제한: actual tracking/TTS alignment·한국어 viseme mapping·blink generator·mask compositor·실제 display timing 미구현. Rhubarb는 후속 오프라인 후보로 live 한국어 품질 검증이 필요하다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
