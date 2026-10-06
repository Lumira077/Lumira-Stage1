# F2020-S01

Jira: https://lumira077.atlassian.net/browse/KR1-171

neutral/happy/sad/listening/thinking/speaking 상태·색상/눈/입 파라미터와 가독성·transition·fallback·끼어들기 계약을 정의한다.

상위 완료조건: S01 계약/평가 기준 검토, S02 실제 renderer/TTS/제어 adapter 및 재현 버전, S03 실제 장비의 표현 품질·통합/성능/안전 증적, S04 실제 사용자/운영/rollback 및 Q1/R1 승인 확보. 합성 입력 합격만으로 전체 완료 판정하지 않는다.

지표: 표정/상태 이해율·transition 가독성·FPS/dropped frame·render p50/p95·취소 후 residual frame·장시간 발열

제한: 실제 디스플레이/GPU/Qt frame loop·blink/brow rendering·event bus·대상 사용자 가독성 평가 미실시. SVG 정적 샘플은 실기 FPS 검증이 아니다.

증적: source/model/asset/hash/license/config/policy version, device/calibration, age/language/environment, sample count, expected/actual, failure/retest, reviewer. 승인 전 수치 목표는 draft이며 실제 참가자 0명, release_ready=false.
